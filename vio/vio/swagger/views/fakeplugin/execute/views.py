# Copyright (c) 2019 VMware, Inc.
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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import json
import requests


class FakeExecute(APIView):

    def post(self, request):
        try:
            reqbody = json.loads(request.body)
            kwargs = {
                "verify": False,
            }
            url = reqbody["url"]
            method = reqbody.get("method", "get").lower()
            kwargs['headers'] = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "x-hm-authorization": "3d1f2ab6:8073:4da4:8f1a:eb2c349ba24",
            }
            kwargs['headers'].update(reqbody.get("headers", {}))
            if reqbody.get("body"):
                kwargs['json'] = reqbody["body"]
            resp = requests.request(method, url, **kwargs)
            respHeaders = resp.headers
            for k in ["Connection", "Keep-Alive", "Transfer-Encoding"]:
                if k in respHeaders:
                    del respHeaders[k]
            try:
                respData = resp.json()
            except Exception:
                respData = resp.content
        except Exception as ex:
            return Response(
                data={"error": str(ex)},
                status=status.HTTP_400_BAD_REQUEST)
        return Response(
            data=respData,
            status=resp.status_code,
            headers=respHeaders,
            content_type=respHeaders.get("Content-Type"))
