# Copyright (c) 2017-2018 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import logging
from rest_framework import status
from rest_framework.response import Response

from vio.pub.msapi import extsys
from vio.pub.exceptions import VimDriverVioException
from vio.pub.utils.syscomm import catalog
from vio.pub.utils.syscomm import verifyKeystoneV2
from vio.pub.utils.syscomm import keystoneVersion
from vio.pub.utils.syscomm import SUCCESS_STATE
from vio.pub.config.config import MSB_SERVICE_PORT, MSB_SERVICE_IP
import json
import requests
from collections import defaultdict
from copy import deepcopy

from vio.swagger.views.proxyplugin.httpclient import BaseClient

logger = logging.getLogger(__name__)

MSB_ADDRESS = MSB_SERVICE_IP + ":" + MSB_SERVICE_PORT + "/api"

NO_TENANTID_SERVICE_TYPE = ['image', 'network', 'cloudformation',
                            'identity', 'dns']


class IdentityVersionLink(BaseClient):

    serverType = 'keystone'

    def get(self, request, vimid):
        (url, headers, _) = self.buildRequest(request, vimid, tail=None,
                                              method="GET")

        try:
            res = self._request(url, method="GET", headers=headers)
            if res.status_code != status.HTTP_200_OK:
                return Response(data={"error": res.data},
                                status=res.status_code)
            res = res.data
            # replace keystone endpoint url with multicloud
            # endpoint url, the default version is V3
            res['version']['links'][0]['href'] = \
                "http://" + MSB_ADDRESS + "/multicloud-vio/v0/" \
                + vimid + "/identity"

        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=res, status=status.HTTP_200_OK)


class IdentityVersionLinkV1(IdentityVersionLink):

    serverType = 'keystone'

    def get(self, request, cloud_owner, cloud_region):
        return super(IdentityVersionLinkV1, self).get(
            request, cloud_owner + "_" + cloud_region)


class IdentityServer(BaseClient):

    serverType = 'keystone'

    def get(self, request, vimid, other=None):

        (url, headers, _) = self.buildRequest(request, vimid, tail=other,
                                              method="GET")

        return self._request(url, method="GET", headers=headers)

    def patch(self, request, vimid, other):

        return self.send(request=request, method="PATCH",
                         vimid=vimid, other=other)

    def post(self, request, vimid, other):

        return self.send(request=request, method="POST",
                         vimid=vimid, other=other)

    def delete(self, request, vimid, other):

        return self.send(request=request, method="DELETE",
                         vimid=vimid, other=other)

    def head(self, request, vimid, other):

        return self.send(request=request, method="HEAD",
                         vimid=vimid, other=other)


class IdentityServerV1(IdentityServer):

    serverType = 'keystone'

    def get(self, request, cloud_owner, cloud_region, other=None):
        return super(IdentityServerV1, self).get(
            request, cloud_owner + "_" + cloud_region, other)

    def post(self, request, cloud_owner, cloud_region, other):
        return super(IdentityServerV1, self).post(
            request, cloud_owner + "_" + cloud_region, other)

    def patch(self, request, cloud_owner, cloud_region, other):
        return super(IdentityServerV1, self).patch(
            request, cloud_owner + "_" + cloud_region, other)

    def put(self, request, cloud_owner, cloud_region, other):
        return super(IdentityServerV1, self).put(
            request, cloud_owner + "_" + cloud_region, other)

    def head(self, request, cloud_owner, cloud_region, other):
        return super(IdentityServerV1, self).head(
            request, cloud_owner + "_" + cloud_region, other)


class TokenView(BaseClient):

    serverType = 'identity'

    def get(self, request, vimid):

        url_path = request.get_full_path()
        if url_path[url_path.rfind("identity"):] != "identity/v3":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            vim_info = extsys.get_vim_by_id(vim_id=vimid)
        except VimDriverVioException as e:
            return Response(data={"error": str(e)}, status=e.status_code)
        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = keystoneVersion(url=vim_info['url'], version="v3")
        logger.info("vimid(%(vimid)s) get keystone url %(url)s ",
                    {"vimid": vimid, "url": url})
        try:
            res = requests.get(url=url, verify=False)
            if res.status_code not in SUCCESS_STATE:
                return Response(data={"error": res.content},
                                status=res.status_code)
            res = res.json()
            res['version']['links'][0]['href'] = \
                "http://" + MSB_ADDRESS + "/multicloud-vio/v0/" \
                + vimid + "/identity/v3"

        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=res, status=status.HTTP_200_OK)

    def delete(self, request, vimid):

        (url, headers, _) = self.buildRequest(request, vimid)

        subject_token = request.META.get("HTTP_X_SUBJECT_TOKEN", "")

        url += "/auth/tokens"
        headers["X-Subject-Token"] = subject_token
        return self._request(url, method="DELETE", headers=headers)

    def post(self, request, vimid):

        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(
                data={'error': 'Fail to decode request body %s.' % e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url_path = request.get_full_path()

        # if request boy formatter match  token v2,
        # It change to use v2 authorization.
        if verifyKeystoneV2(create_req):
            return _keystoneV2Token(url_path, vimid,
                                    create_req=create_req)

        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)
        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if url_path[url_path.rfind("identity"):] != "identity/v3/auth/tokens":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        url = keystoneVersion(url=vim_info['url'], version="v3")
        url += "/auth/tokens"
        headers = {"Content-Type": "application/json"}
        logger.info("vimid(%(vimid)s) request V3 token url %(url)s ",
                    {"vimid": vimid, "url": url})

        try:
            res = requests.post(url=url, data=json.dumps(create_req),
                                headers=headers, verify=False)
            if res.status_code not in SUCCESS_STATE:
                return Response(data={"error": res.content},
                                status=res.status_code)

            tokenInfo = res.json()
            resHeader = dict(res.headers)
        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:

            tenantid = tokenInfo['token']['project']['id']
            vimEndpoints = defaultdict(dict)

            for i in tokenInfo['token']['catalog']:
                for j in i['endpoints']:
                    tmp = j['url']
                    ends = deepcopy(j['url'])
                    ends = ends.split("/")
                    version = "/" + ends[3] if len(ends) > 3 else ""
                    ends = ends[0] + "//" + ends[2] + version
                    vimEndpoints[i['name']][j['interface']] = ends
                    res = tmp.split("/")
                    if i['type'] in NO_TENANTID_SERVICE_TYPE:
                        if i['type'] != 'identity':
                            res[2] = MSB_ADDRESS + "/multicloud-vio/v0/" + \
                                vimid + "/" + i['name']
                        else:
                            #  use identity instead of keystone
                            res[2] = MSB_ADDRESS + "/multicloud-vio/v0/" + \
                                vimid + "/" + i['type']
                    else:
                        res[2] = MSB_ADDRESS + "/multicloud-vio/v0/" + \
                            vimid + "/" + i['name'] + "/" + tenantid
                    j['url'] = "http:" + "//" + res[2]

            logger.info("vimid(%(vimid)s) service enpoints %(endpoint)s ", {
                    "vimid": vimid, "endpoint": vimEndpoints})
            tokenInfo['token']['value'] = resHeader['X-Subject-Token']
            catalog.storeEndpoint(vimid=vimid, endpoints=vimEndpoints)

        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        Res = Response(data=tokenInfo, status=status.HTTP_200_OK)
        Res['X-Subject-Token'] = resHeader['X-Subject-Token']
        return Res


class TokenViewV1(TokenView):

    serverType = 'identity'

    def get(self, request, cloud_owner, cloud_region):
        return super(TokenViewV1, self).get(
            request, cloud_owner + "_" + cloud_region)

    def post(self, request, cloud_owner, cloud_region):
        return super(TokenViewV1, self).post(
            request, cloud_owner + "_" + cloud_region)

    def delete(self, request, cloud_owner, cloud_region):
        return super(TokenViewV1, self).delete(
            request, cloud_owner + "_" + cloud_region)


class TokenV2View(BaseClient):

    serverType = "identity"

    def get(self, request, vimid):

        url_path = request.get_full_path()
        if url_path[url_path.rfind("identity"):] != "identity/v2.0":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            vim_info = extsys.get_vim_by_id(vim_id=vimid)
        except VimDriverVioException as e:
            return Response(data={"error": str(e)}, status=e.status_code)
        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # replace to v2.0
        url = keystoneVersion(url=vim_info['url'], version="v2.0")
        logger.info("vimid(%(vimid)s) get keystoneV2 url %(url)s ",
                    {"vimid": vimid, "url": url})
        try:
            res = requests.get(url=url, verify=False)
            if res.status_code not in SUCCESS_STATE:
                return Response(data={"error": res.content},
                                status=res.status_code)
            res = res.json()
            res['version']['links'][0]['href'] = \
                "http://" + MSB_ADDRESS + "/multicloud-vio/v0/" \
                + vimid + "/identity/v2.0"

        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=res, status=status.HTTP_200_OK)

    def post(self, request, vimid):

        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(
                data={'error': 'Fail to decode request body %s.' % e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url_path = request.get_full_path()

        return _keystoneV2Token(url=url_path,
                                vimid=vimid,
                                create_req=create_req)


class TokenV2ViewV1(TokenV2View):

    serverType = 'identity'

    def get(self, request, cloud_owner, cloud_region):
        return super(TokenV2ViewV1, self).get(
            request, cloud_owner + "_" + cloud_region)

    def post(self, request, cloud_owner, cloud_region):
        return super(TokenV2ViewV1, self).post(
            request, cloud_owner + "_" + cloud_region)


def _keystoneV2Token(url, vimid=None, create_req=None):

    try:
        vim_info = extsys.get_vim_by_id(vimid)
    except VimDriverVioException as e:
        return Response(data={'error': str(e)}, status=e.status_code)
    except Exception as e:
        logging.exception("error %s" % e)
        return Response(data={"error": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if url[url.rfind("identity"):] not in ["identity/v3/tokens",
                                           "identity/v2.0/tokens"]:
        return Response(data={"error": "method not allowed"},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
    # replace to v2.0
    url = keystoneVersion(url=vim_info["url"], version="v2.0")
    url += "/tokens"
    headers = {"Content-Type": "application/json"}
    logger.info("vimid(%(vimid)s) request V2 token url %(url)s ",
                {"vimid": vimid, "url": url})

    try:
        res = requests.post(url=url, data=json.dumps(create_req),
                            headers=headers, verify=False)
        if res.status_code not in SUCCESS_STATE:
            return Response(data={"error": res.content},
                            status=res.status_code)
        tokenInfo = res.json()
    except Exception as e:
        logging.exception("error %s" % e)
        return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    try:

        tenantid = tokenInfo['access']['token']['tenant']['id']
        vimEndpoints = defaultdict(dict)
        for cal in tokenInfo['access']['serviceCatalog']:
            # endpoint urls
            item = cal['endpoints'][0]
            adminurl = deepcopy(item['adminURL']).split('/')
            internalurl = deepcopy(item['internalURL']).split('/')
            publicurl = deepcopy(item['publicURL']).split('/')
            # VIO identity url use v3 as default even got token by v2,
            # need change to v2.0
            if cal['type'] == 'identity':
                adminurl[-1] = "v2.0"
                publicurl[-1] = "v2.0"
                internalurl[-1] = "v2.0"
            adminurl = adminurl[0] + "//" + adminurl[2] + (
                "/" + adminurl[3] if len(adminurl) > 3 else "")
            internalurl = internalurl[0] + "//"+internalurl[2] + (
                "/" + internalurl[3] if len(internalurl) > 3 else "")
            publicurl = publicurl[0] + "//"+publicurl[2] + (
                "/" + publicurl[3] if len(publicurl) > 3 else "")

            for (key, urlname) in zip(('admin', 'internal', 'public'),
                                      (adminurl, internalurl,
                                      publicurl)):
                vimEndpoints[cal['name']][key] = urlname

            if cal['type'] in NO_TENANTID_SERVICE_TYPE:
                name = cal['name'] if cal['type'] != 'identity' \
                    else cal['type']
                for i in ("adminURL", "internalURL", "publicURL"):
                    item[i] = "http://" + MSB_ADDRESS + \
                                "/multicloud-vio/v0/" + vimid + "/" + name
            else:
                for i in ("adminURL", "internalURL", "publicURL"):
                    item[i] = "http://" + MSB_ADDRESS + \
                                "/multicloud-vio/v0/" + vimid + \
                                "/" + cal["name"] + "/"+tenantid

        logger.info("vimid(%(vimid)s) service enpoints %(endpoint)s ", {
                    "vimid": vimid, "endpoint": vimEndpoints})
        catalog.storeEndpoint(vimid=vimid, endpoints=vimEndpoints)

    except Exception as e:
        logging.exception("error %s" % e)
        return Response(data={'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    Res = Response(data=tokenInfo, status=status.HTTP_200_OK)
    return Res
