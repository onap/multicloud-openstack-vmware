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

class ComputeServer(BaseClient):
    serverType = "compute"


    def get(self,request,vimid,tenantid,other):

        (url, headers, _) = self.buildRequest(request, vimid, tenantid=tenantid,tail=other)
        query = ""
        for k, v in request.GET.items():
            query += (k + "=" + v)
            query += "&"

        if query != "":
            query = query[:-1]
            url += "?" + query
        return self._request(url, method="GET", headers=headers)

    def post(self,request,vimid,tenantid,other):

        return  self.send(request=request,method="POST",vimid=vimid,tenantid=tenantid,other=other)

    def put(self,request,vimid,tenantid,other):

        return  self.send(request=request,method="PUT",vimid=vimid,tenantid=tenantid,other=other)

    def delete(self,request,vimid,tenantid,other):

        return  self.send(request=request,method="DELETE",vimid=vimid,tenantid=tenantid,other=other)
