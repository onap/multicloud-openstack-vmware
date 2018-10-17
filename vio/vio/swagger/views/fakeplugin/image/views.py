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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import json

from vio.swagger.views.fakeplugin.fakeData.fakeResponse import image_detail
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import list_image
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import image_schema
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import image_version
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import upload_image

false = "false"
null = "null"
true = "true"


class FakeImageDetail(APIView):

    def get(self, request, imageid):

        data = image_detail()
        return Response(data=data, status=status.HTTP_200_OK)


class FakeImage(APIView):

    def get(self, request):

        data = list_image()
        return Response(data=data, status=status.HTTP_200_OK)


class FakeImageSchema(APIView):

    def get(self, request):
        data = image_schema()
        return Response(data=data, status=status.HTTP_200_OK)


class FakeImageVersion(APIView):

    def get(self, request):

        data = image_version()
        return Response(data=data, status=status.HTTP_200_OK)


class FakeImageDownload(APIView):

    def get(self, request, imageid):

        data = image_detail()
        return Response(data=data, status=status.HTTP_200_OK)


class FakeImageUpload(APIView):

    def post(self, request):
        req = json.loads(request.body)
        data = upload_image(dict(req))
        return Response(data=data, status=status.HTTP_201_CREATED)
