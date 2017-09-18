from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from vio.swagger.views.fakeplugin.fakeData.fakeRespone import neutron_version
from vio.swagger.views.fakeplugin.fakeData.fakeRespone import neutron_detail
from vio.swagger.views.fakeplugin.fakeData.fakeRespone import network_list


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