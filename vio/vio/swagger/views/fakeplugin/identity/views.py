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

import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from vio.swagger.views.fakeplugin.fakeData.fakeResponse import \
    keystone_token
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import \
    keystone_tokenV2
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import \
    keystone_version
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import \
    keystone_version2
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import list_projects
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import show_project
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import get_tenants


class FakeProjects(APIView):

    def get(self, request, projectid=None):

        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        if projectid:
            data = show_project(token, projectid)
        else:
            data = list_projects(token)

        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)


class FakeToken(APIView):

    def get(self, request):

        return Response(data=keystone_version(),
                        status=status.HTTP_200_OK)

    def post(self, request):

        try:
            create_req = json.loads(request.body)
            tennatid = create_req['auth']['scope']['project']['id']
        except Exception as e:
            return Response(
                data={'error': 'Invalidate request body %s.' % e},
                status=status.HTTP_400_BAD_REQUEST)

        url_path = request.get_full_path()

        if url_path[url_path.rfind("identity"):] != \
                "identity/v3/auth/tokens":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        tokeninfo = keystone_token(teanatid=tennatid)
        res = Response(data=tokeninfo, status=status.HTTP_201_CREATED)
        res['X-Subject-Token'] = tokeninfo['token']['value']
        return res


class FakeTokenV2(APIView):

    def get(self, request):

        return Response(data=keystone_version2(),
                        status=status.HTTP_200_OK)

    def post(self, request):

        try:
            json.loads(request.body)
        except Exception as e:
            return Response(
                data={'error': 'Invalidate request body %s.' % e},
                status=status.HTTP_400_BAD_REQUEST)

        url_path = request.get_full_path()

        if url_path[url_path.rfind("identity"):] != \
                "identity/v2.0/tokens":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        tokeninfo = keystone_tokenV2()
        return Response(data=tokeninfo, status=status.HTTP_200_OK)


class FakeTenants(APIView):

    def get(self, request, projectid=None):

        data = get_tenants()
        return Response(data=data, status=status.HTTP_200_OK)
