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

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from vio.swagger.views.fakeplugin.fakeData.fakeResponse import neutron_version
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import neutron_detail
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import network_list


class FakeNeutron(APIView):

    def get(self, request):
        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = neutron_version(token=token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)


class FakeNeutronNetwork(APIView):

    def get(self, request):
        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = network_list(token=token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])
        return Response(data=data, status=status.HTTP_200_OK)


class FakeNeutronDetail(APIView):

    def get(self, request, netid):
        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = neutron_detail(token=token, netid=netid)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)
