# Copyright (c) 2018 VMware, Inc.
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
import mock
import unittest

from vio.swagger.views.fakeplugin.nova import views
from vio.swagger.views.fakeplugin.fakeData import fakeResponse

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00" \
        "TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
        "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4" \
        "bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"

Server = "764e369e-a874-4401-b7ce-43e4760888da"


class TestFakeNovaServer(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeNovaServer()

    def tearDown(self):
        fakeResponse.serverMapps[Server]['status'] = "ACTIVE"

    @mock.patch.object(fakeResponse, "show_serverDetail")
    def test_get_server(self, mock_show_serverDetail):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_show_serverDetail.return_value = {
            "server-id": "1234abcd"
        }
        resp = self.view.get(req, "abcd", Server)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(fakeResponse, "delete_server")
    def test_delete_server(self, mock_delete_server):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_delete_server.return_value = {}
        resp = self.view.delete(req, "abcd", Server)
        self.assertEqual(204, resp.status_code)

    def test_list_servers(self):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        resp = self.view.get(req, "abcd")
        self.assertEqual(200, resp.status_code)

    def test_list_servers_unauth(self):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": "invalid"
        }
        resp = self.view.get(req, "abcd")
        self.assertEqual(401, resp.status_code)

    def test_operate_server_stop(self):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        req.body = json.dumps({
            "os-stop": {}
        })
        resp = self.view.post(req, "abcd", Server)
        self.assertEqual(202, resp.status_code)
        self.assertEqual(
            "POWERING_OFF", fakeResponse.serverMapps[Server]['status'])

    def test_operate_server_start(self):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        req.body = json.dumps({
            "os-start": {}
        })
        fakeResponse.serverMapps[Server]['status'] = "SHUTDOWN"
        resp = self.view.post(req, "abcd", Server)
        self.assertEqual(202, resp.status_code)
        self.assertEqual(
            "POWERING_ON", fakeResponse.serverMapps[Server]['status'])


class TestFakeNovaHypervisors(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeNovaHypervisors()

    @mock.patch.object(fakeResponse, "get_oshypervisor")
    def test_get_hypervisor(self, mock_get_oshypervisor):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_get_oshypervisor.return_value = {
            "hypervisor": "1234abcd"
        }
        resp = self.view.get(req, "abcd")
        self.assertEqual(200, resp.status_code)


class TestFakeNovaAggregate(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeNovaAggregate()

    @mock.patch.object(fakeResponse, "get_osaggregates")
    def test_get_aggregate(self, mock_get_osaggregates):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_get_osaggregates.return_value = {
            "osaggregates": "1234abcd"
        }
        resp = self.view.get(req, "abcd")
        self.assertEqual(200, resp.status_code)


class TestFakeNovaServerDetail(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeNovaServerDetail()

    @mock.patch.object(fakeResponse, "get_serverdetail")
    def test_get_server_detail(self, mock_get_serverdetail):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_get_serverdetail.return_value = {
            "servers": "1234abcd"
        }
        resp = self.view.get(req, "abcd")
        self.assertEqual(200, resp.status_code)


class TestFakeFlavorDetail(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeFlavorDetail()

    @mock.patch.object(fakeResponse, "get_flavors")
    def test_get_flavor_detail(self, mock_get_flavors):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_get_flavors.return_value = {
            "flavors": "1234abcd"
        }
        resp = self.view.get(req, "abcd", "1234")
        self.assertEqual(200, resp.status_code)


class TestFakeFlavorList(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeFlavorList()

    @mock.patch.object(fakeResponse, "list_flavors")
    def test_get_flavor_list(self, mock_list_flavors):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_list_flavors.return_value = {
            "flavors": "1234abcd"
        }
        resp = self.view.get(req, "abcd")
        self.assertEqual(200, resp.status_code)


class TestFakeCapacity(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeCapacity()

    def test_get_capacity(self):
        resp = self.view.post(mock.Mock())
        self.assertEqual(200, resp.status_code)
