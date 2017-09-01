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

from vio.swagger.views.proxyplugin.httpclient import BaseClient


class VolumeServer(BaseClient):

    serverType = "cinder"

    def get(self, request, vimid, tenantid, other):

        return self.send(request=request, method="GET", vimid=vimid,
                         tenantid=tenantid, other=other)

    def post(self, request, vimid, tenantid, other):

        return self.send(request=request, method="POST", vimid=vimid,
                         tenantid=tenantid, other=other)

    def put(self, request, vimid, tenantid, other):

        return self.send(request=request, method="PUT", vimid=vimid,
                         tenantid=tenantid, other=other)

    def delete(self, request, vimid, tenantid, other):

        return self.send(request=request, method="DELETE", vimid=vimid,
                         tenantid=tenantid, other=other)

    def patch(self, request, vimid, tenantid, other):

        return self.send(request=request, method="PATCH", vimid=vimid,
                         tenantid=tenantid, other=other)


class VolumeServer2(VolumeServer):
    serverType = "cinderv2"


class VolumeServer3(VolumeServer):
    serverType = "volumev3"
