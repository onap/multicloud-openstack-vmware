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


class DesignateVersionLink(BaseClient):

    serverType = 'designate'

    def get(self, request, vimid):
        (url, headers, _) = self.buildRequest(request, vimid, tail=None,
                                              method="GET")

        try:
            res = self._request(url, method="GET", headers=headers)
            if res.status_code != status.HTTP_200_OK:
                return Response(data={"error": res.data},
                                status=res.status_code)
            res = res.data
            # replace designate endpoint url with multicloud
            # endpoint url.
            # Look: this may contains many version
            for item in res['versions']['values']:

                version = item['id']
                item['links'][0]['href'] = \
                    "http://" + MSB_ADDRESS + "/multicloud-vio/v0/" \
                    + vimid + "/designate/" + version

        except Exception as e:
            logging.exception("error %s" % e)
            return Response(data={"error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=res, status=status.HTTP_200_OK)


class DesignateServer(BaseClient):

    serverType = "designate"

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
