import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from vio.swagger.views.fakeplugin.fakeData.content import keystoneToken
from vio.swagger.views.fakeplugin.fakeData.content import keystoneVersion
from vio.swagger.views.fakeplugin.fakeData.content import ListProjects
from vio.swagger.views.fakeplugin.fakeData.content import showProject


class FakeProjects(APIView):

    def get(self, request, projectid=None):

        data = ""
        token = request.META.get("HTTP_X_AUTH_TOKEN", None)
        if projectid:
            data = showProject(token, projectid)
        else:
            data = ListProjects(token)

        if 'error' in data:
            return Response(data=data['error']['message'],
                            status=data['error']['code'])

        return Response(data=data, status=status.HTTP_200_OK)

    def patch(self, request, projectid):
        return Response()

    def post(self, request):
        return Response()

    def delete(self, request, projectid):
        return Response()


class FakeToken(APIView):

    def get(self, request):

        return Response(data=keystoneVersion(), status=status.HTTP_200_OK)

    def post(self, request):

        try:
            create_req = json.loads(request.body)
            tennatid = create_req['auth']['scope']['project']['id']
        except Exception as e:
            return Response(data={'error': 'Invalidate request body %s.' % e},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        url_path = request.get_full_path()
        if url_path[url_path.rfind("identity"):] != "identity/v3/auth/tokens":
            return Response(data={"error": "method not allowed"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)

        tokeninfo = keystoneToken(teanatid=tennatid)
        res = Response(data=tokeninfo, status=status.HTTP_201_CREATED)
        res['X-Subject-Token'] = tokeninfo['token']['value']
        return res
