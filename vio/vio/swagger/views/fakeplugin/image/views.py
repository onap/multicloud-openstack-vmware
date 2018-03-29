
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
