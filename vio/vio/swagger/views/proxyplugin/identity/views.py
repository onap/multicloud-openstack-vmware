# Copyright (c) 2017 VMware, Inc.
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
from vio.pub.config.config import MSB_SERVICE_PORT, MSB_SERVICE_IP
import json
import requests
from collections import defaultdict
from copy import deepcopy

from vio.swagger.views.proxyplugin.httpclient import BaseClient

logger = logging.getLogger(__name__)

MSB_ADDRESS = MSB_SERVICE_IP + ":" + MSB_SERVICE_PORT + "/api"


class IdentityServer(BaseClient):

    serverType = 'keystone'

    def get(self, request, vimid, other=None):

        (url, headers, _) = self.buildRequest(request, vimid, tail=other)

        query = ""
        for k, v in request.GET.items():
            query += (k + "=" + v)
            query += "&"

        if query != "":
            query = query[:-1]
            url += "/?" + query
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

        keystoneURL = vim_info['url']
        logger.info("vimid(%(vimid)s) get keystone url %(url)s ",
                    {"vimid": vimid, "url": keystoneURL})
        try:
            res = requests.get(url=keystoneURL)
            if res.status_code != status.HTTP_200_OK:
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

        url_path = request.get_full_path()
        if url_path[url_path.rfind("identity"):] != "identity/v3/auth/tokens":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(
                data={'error': 'Fail to decode request body %s.' % e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)
        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url = vim_info['url'] + "/auth/tokens"
        headers = {"Content-Type": "application/json"}
        logger.info("vimid(%(vimid)s) request token url %(url)s ",
                    {"vimid": vimid, "url": url})

        try:
            res = requests.post(url=url, data=json.dumps(
                create_req), headers=headers)
            if res.status_code != status.HTTP_201_CREATED:
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
                    if i['type'] in ['image', 'network',
                                     'cloudformation', 'identity']:
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
        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        logger.info("vimid(%(vimid)s) service enpoints %(endpoint)s ", {
                    "vimid": vimid, "endpoint": vimEndpoints})
        tokenInfo['token']['value'] = resHeader['X-Subject-Token']
        catalog.storeEndpoint(vimid=vimid, endpoints=vimEndpoints)
        Res = Response(data=tokenInfo, status=status.HTTP_200_OK)
        Res['X-Subject-Token'] = resHeader['X-Subject-Token']
        return Res
