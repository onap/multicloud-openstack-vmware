import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from vio.swagger.views.fakeplugin.fakeData.fakeResponse import get_oshypervisor
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import get_servers
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import show_serverDetail
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import operator_server
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import delete_server
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import create_instance
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import get_serverdetail
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import get_osaggregates
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import hypervisor_uptime
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import get_flavors
from vio.swagger.views.fakeplugin.fakeData.fakeResponse import list_flavors


false = "false"
true = "true"


class FakeNovaServer(APIView):

    def get(self, request, tenantid, serverid=None):

        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        if serverid:
            data = show_serverDetail(token, tenantid=tenantid,
                                    serverid=serverid)

        else:
            data = get_servers(token=token, tenantid=tenantid)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, tenantid, serverid=None):

        data = ""
        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(data={
                'error': 'Invalidate request body %s.' % e},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        if serverid:
            data = operator_server(token, serverid,
                                   action=create_req.keys()[0])
        # create server
        elif serverid is None:

            data = create_instance(token, json=create_req)
            if 'error' in data:
                return Response(data=data['error']['message'],
                                status=data['error']['code'])
            return Response(data=data, status=status.HTTP_202_ACCEPTED)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, tenantid, serverid):

        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = delete_server(token, serverid)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class FakeNovaHypervisors(APIView):

    def get(self, request, tenantid, hyperid=None):
        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = get_oshypervisor(token, hyperid)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)


class FakeNovaAggregate(APIView):

    def get(self, request, tenantid):
        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = get_osaggregates(token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)


class FakeNovaHypervisorsUptime(APIView):

    def get(self, request, tenantid, hyperid):

        data = hypervisor_uptime()
        return Response(data=data, status=status.HTTP_200_OK)


class FakeNovaServerDetail(APIView):

    def get(self, request, tenantid):
        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = get_serverdetail(token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)


class FakeFlavorDetail(APIView):

    def get(self, request, tenantid, flavorid):

        data = get_flavors(flag=flavorid)
        return Response(data=data, status=status.HTTP_200_OK)


class FakeFlavorList(APIView):

    def get(self, request, tenantid):

        data = list_flavors()
        return Response(data=data, status=status.HTTP_200_OK)
