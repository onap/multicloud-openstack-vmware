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

import logging
import requests
import json
import socket
import time

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from vio.pub.utils.syscomm import catalog, jsonResponse
import vio.pub.exceptions as exceptions


logger = logging.getLogger(__name__)


class TCPKeepAliveAdapter(requests.adapters.HTTPAdapter):
    """The custom adapter used to set TCP Keep-Alive on all connections."""

    def init_poolmanager(self, *args, **kwargs):
        if 'socket_options' not in kwargs \
            and tuple(int(v) for v in requests.__version__.split('.')) \
                >= (2, 4, 1):
            socket_options = [
                # Keep Nagle's algorithm off
                (socket.IPPROTO_TCP, socket.TCP_NODELAY, 1),
                # Turn on TCP Keep-Alive
                (socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1),
            ]

            if hasattr(socket, 'TCP_KEEPIDLE'):
                socket_options += [
                    # Wait 60 seconds before sending keep-alive probes
                    (socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 60)
                ]

            if hasattr(socket, 'TCP_KEEPINTVL'):
                socket_options += [
                    # Send keep-alive probes every 15 seconds
                    (socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 15),
                ]

            kwargs['socket_options'] = socket_options
        super(TCPKeepAliveAdapter, self).init_poolmanager(*args, **kwargs)


class BaseClient(APIView):

    def __init__(self):
        super(BaseClient, self).__init__()

        self.session = requests.Session()
        for schema in list(self.session.adapters):
            self.session.mount(schema, TCPKeepAliveAdapter())

    def buildRequest(self, request, vimid, tenantid="", tail=None,
                     method=None):

        headers = {}
        preUrl = catalog.getEndpointBy(
            vimid, serverType=self.serverType, interface="public")

        token = request.META.get('HTTP_X_AUTH_TOKEN', "")
        tail = "/" + tail if tail else ""
        tenantid = "/" + tenantid if tenantid else ""
        endPointURL = preUrl + tenantid + tail if preUrl else ""

        headers["X-Auth-Token"] = token
        headers["X-Subject-Token"] = token
        headers['Content-Type'] = request.META.get(
            "CONTENT_TYPE", "application/json")

        if method == "GET" and preUrl is not None:
            # append parameters in url path
            query = ""
            for k, v in request.GET.items():
                query += (k + "=" + v)
                query += "&"

            if query != "":
                query = query[:-1]
                endPointURL += "?" + query

        try:
            json_req = json.loads(request.body)
        except Exception:
            json_req = ""

        return endPointURL, headers, json_req

    def _request(self, url, method, redirect=20,
                 connect_retries=0, connect_retry_delay=0.5, **kwargs):

        try:
            try:
                # Authenticated failed If it cann't get
                # endpoint from cache
                if url == "":
                    return Response(data="Unauthenticated",status=401)
                logger.info("%(method)s Request to %(url)s ",
                            {'url': url, 'method': method})
                resp = self.session.request(
                    method, url, verify=False, timeout=30, **kwargs)
            except requests.exceptions.SSLError as e:
                msg = 'SSL exception connecting to %(url)s: %(error)s' % {
                    'url': url, 'error': e}
                raise exceptions.SSLError(msg)
            except requests.exceptions.Timeout:
                msg = 'Request to %s timed out' % url
                raise exceptions.ConnectTimeout(msg)
            except requests.exceptions.ConnectionError as e:
                msg = 'Unable to establish connection to %s: %s' % (url, e)
                raise exceptions.ConnectionError(msg)
            except requests.exceptions.RequestException as e:
                msg = 'Unexpected exception for %(url)s: %(error)s' % {
                    'url': url, 'error': e}
                raise exceptions.UnknownConnectionError(msg, e)

        except exceptions.RetriableConnectionFailure as e:
            if connect_retries <= 0:
                return Response(data={"error": str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            logger.info('Failure: %(e)s. Retrying in %(delay).1fs.',
                        {'e': e, 'delay': connect_retry_delay})
            time.sleep(connect_retry_delay)

            return self._request(
                url, method, redirect,
                connect_retries=connect_retries - 1,
                connect_retry_delay=connect_retry_delay * 2,
                **kwargs)

        if resp.status_code in [301, 302, 303, 305, 307, 308]:

            if isinstance(redirect, bool):
                redirect_allowed = redirect
            else:
                redirect -= 1
                redirect_allowed = redirect >= 0

            if not redirect_allowed:
                return resp

            try:
                location = resp.headers['location']
            except KeyError:
                logger.warning("Failed to redirect request to %s as new "
                               "location was not provided.", resp.url)
                pass

            else:
                new_resp = self._request(
                    location, method, redirect,
                    connect_retries=connect_retries,
                    **kwargs)

                if not isinstance(new_resp.history, list):
                    new_resp.history = list(new_resp.history)
                new_resp.history.insert(0, resp)
                resp = new_resp

        data, content_type = jsonResponse(resp.content)
        return Response(data=data, status=resp.status_code,
                        content_type=content_type)

    def send(self, request, method, vimid, tenantid="", other="", **kwargs):


        (url, headers, data) = self.buildRequest(
            request, vimid, tenantid=tenantid, tail=other)
        kwargs.setdefault('headers', headers)

        if method in ["POST", "PUT", "PATCH"]:
            kwargs.setdefault('data', json.dumps(data, encoding='utf-8'))

        return self._request(url, method, **kwargs)

    def get(self, request, vimid):
        raise NotImplementedError()

    def post(self, request, vimid):
        raise NotImplementedError()

    def put(self, request, vimid):
        raise NotImplementedError()

    def patch(self, request, vimid):
        raise NotImplementedError()

    def delete(self, request, vimid):
        raise NotImplementedError()

    def head(self, request, vimid):
        raise NotImplementedError()
