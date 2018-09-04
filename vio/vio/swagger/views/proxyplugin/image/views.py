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
from vio.swagger.views.proxyplugin.httpclient import BaseClient
from vio.pub.config.config import MSB_SERVICE_PORT, MSB_SERVICE_IP


logger = logging.getLogger(__name__)


MSB_ADDRESS = MSB_SERVICE_IP + ":" + MSB_SERVICE_PORT + "/api"


class ImageVersionLink(BaseClient):

    serverType = 'glance'

    def get(self, request, vimid):
        (url, headers, _) = self.buildRequest(request, vimid, tail=None,
                                              method="GET")

        try:
            res = self._request(url, method="GET", headers=headers)
            res = res.data
            # replace glance endpoint url with multicloud
            # endpoint url.
            # Look: this may contains many version
            for item in res['versions']:

                version = item['id']
                version = version[:2] if len(version) > 2 else version
                item['links'][0]['href'] = \
                    "http://" + MSB_ADDRESS + "/multicloud-vio/v0/" \
                    + vimid + "/glance//" + version + "/"

        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # MARK: this response status is 301
        return Response(data=res, status=status.HTTP_300_MULTIPLE_CHOICES)


class ImageVersionLinkV1(ImageVersionLink):

    serverType = 'glance'

    def get(self, request, cloud_owner, cloud_region):
        return super(ImageVersionLinkV1, self).get(
            request, cloud_owner + "_" + cloud_region)


class ImageServer(BaseClient):

    serverType = "glance"

    def get(self, request, vimid, other=None):

        (url, headers, _) = self.buildRequest(request, vimid, tail=other,
                                              method="GET")

        return self._request(url, method="GET", headers=headers)

    def post(self, request, vimid, other):

        return self.send(request=request, method="POST",
                         vimid=vimid, other=other)

    def patch(self, request, vimid, other):

        return self.send(request=request, method="PATCH",
                         vimid=vimid, other=other)

    def put(self, request, vimid, other):

        return self.send(request=request, method="PUT",
                         vimid=vimid, other=other)

    def delete(self, request, vimid, other):

        return self.send(request=request, method="DELETE",
                         vimid=vimid, other=other)


class ImageServerV1(ImageServer):

    serverType = 'glance'

    def get(self, request, cloud_owner, cloud_region, other=None):
        return super(ImageServerV1, self).get(
            request, cloud_owner + "_" + cloud_region, other)

    def post(self, request, cloud_owner, cloud_region, other):
        return super(ImageServerV1, self).post(
            request, cloud_owner + "_" + cloud_region, other)

    def patch(self, request, cloud_owner, cloud_region, other):
        return super(ImageServerV1, self).patch(
            request, cloud_owner + "_" + cloud_region, other)

    def put(self, request, cloud_owner, cloud_region, other):
        return super(ImageServerV1, self).put(
            request, cloud_owner + "_" + cloud_region, other)

    def delete(self, request, cloud_owner, cloud_region, other):
        return super(ImageServerV1, self).delete(
            request, cloud_owner + "_" + cloud_region, other)
