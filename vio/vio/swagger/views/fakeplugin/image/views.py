
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from vio.swagger.views.fakeplugin.fakeData.fakeResponse import image_detail
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import list_image
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import image_schema

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
