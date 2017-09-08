import json

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from vio.swagger.views.fakeplugin.fakeData.content import GetOSHypervisor
from vio.swagger.views.fakeplugin.fakeData.content import getServers
from vio.swagger.views.fakeplugin.fakeData.content import showServerDetail
from vio.swagger.views.fakeplugin.fakeData.content import operator_server
from vio.swagger.views.fakeplugin.fakeData.content import deleteServer
from vio.swagger.views.fakeplugin.fakeData.content import createInstance


class FakeNovaServer(APIView):

    def get(self, request, tenantid, serverid=None):

            token = request.META.get("HTTP_X_AUTH_TOKEN", "")
            if serverid:
                data = showServerDetail(token, tenantid=tenantid,
                                        serverid=serverid)

            else:
                data = getServers(token=token, tenantid=tenantid)
            if 'error' in data:
                return Response(data=data['error']['message'],
                                 status=data['error']['code'])

            return Response(data=data,status=status.HTTP_200_OK)

    def put(self, request, vimid, tenantid, server_id):

            return Response()

    def post(self, request, tenantid, serverid=None):

        data = ""
        try:
            create_req = json.loads(request.body)
        except Exception as e:
            return Response(data={'error':
                            'Invalidate request body %s.' % e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        if serverid:
            data = operator_server(token, serverid,
                                   action=create_req.keys()[0])
            if 'error' in data:
                return Response(data=data['error']['message'],
                                status=data['error']['code'])
            return Response(data=data, status=status.HTTP_202_ACCEPTED)
        # create server
        elif serverid == None:
            data = createInstance(token,json=create_req)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, tenantid, serverid):

        token = request.META.get("HTTP_X_AUTH_TOKEN","")
        data = deleteServer(token, serverid)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_204_NO_CONTENT)


class FakeNovaHypervisors(APIView):

    def get(self, request, tenantid):

        token = request.META.get("HTTP_X_AUTH_TOKEN", "")
        data = GetOSHypervisor(token)
        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)
