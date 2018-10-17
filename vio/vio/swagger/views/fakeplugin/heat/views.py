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

from vio.swagger.views.fakeplugin.fakeData.fakeResponse import getAllStacks
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import showStack
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import showStackByID
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import createStack
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import deleteStack
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import \
    getStackResource
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import \
    createStackPreview


class FakeHeatResources(APIView):

    def get(self, request, tenantid, stack_id=None):
        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        data = getStackResource(token=token, stack_id=stack_id)

        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)


class FakeHeatServicePreview(APIView):

    def post(self, request, tenantid=None):
        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        try:
            if tenantid is None:
                return Response(data="bad request",
                                status=status.HTTP_400_BAD_REQUEST)
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(data="servers error {}".format(str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        name = create_req['stack_name']
        data = createStackPreview(stack_name=name,
                                  token=token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_201_CREATED)


class FakeHeatService(APIView):

    def get(self, request, tenantid, stackName=None, stackID=None):
        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        data = ""
        if stackName is None and stackID is None:
            data = getAllStacks(token=token)
        elif stackName and stackID:
            data = showStackByID(stack_name=stackName,
                                 stack_id=stackID, token=token)
        elif stackName:
            data = showStack(stack_name=stackName, token=token)

        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, tenantid=None):
        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        try:
            if tenantid is None:
                return Response(data="bad request",
                                status=status.HTTP_400_BAD_REQUEST)
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(data="servers error {}".format(str(e)),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        name = create_req['stack_name']

        data = createStack(stack_name=name, token=token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_201_CREATED)

    def put(self, request, vimid):
        pass

    def delete(self, request, tenantid, stackName=None, stackID=None):

        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        data = deleteStack(stack_id=stackID, token=token)

        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class FakeInfraWorkloadAPIGet(APIView):

    def get(self, request, workload_id):
        if workload_id != "fdae10c6-664c-48e2-9e86-7bc2d7e42c26":
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = {
            "template_type": "heat",
            "workload_id": "fdae10c6-664c-48e2-9e86-7bc2d7e42c26",
        }

        return Response(data=data, status=status.HTTP_200_OK)

    def delete(self, request, workload_id):
        if workload_id != "fdae10c6-664c-48e2-9e86-7bc2d7e42c26":
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)


class FakeInfraWorkloadAPIPost(APIView):

    def post(self, request):
        data = {
            "template_type": "heat",
            "workload_id": "fdae10c6-664c-48e2-9e86-7bc2d7e42c26",
        }

        return Response(data=data, status=status.HTTP_200_OK)
