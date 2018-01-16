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

import unittest
import json
import mock
from rest_framework import status
from vio.swagger.views.port.views import CreatePortView, DeletePortView


from vio.pub.utils import syscomm
from vio.pub.vim.vimapi.network.OperatePort import OperatePort


class PortViewTest(unittest.TestCase):

    def setUp(self):
        self.cpv = CreatePortView()
        self.dpv = DeletePortView()

    def tearDown(self):
        pass

    @mock.patch.object(OperatePort, 'list_port')
    @mock.patch.object(syscomm, 'fun_name')
    def test_port_list_view(self, mock_list_port, mock_fun_name):

        # mock_fun_name.return_value = "fun_name"
        mock_list_port.return_value = {'vimName': 'name1', 'vimId': 1}

        class Request:
            def __init__(self, query_params, body, method):
                self.query_params = query_params
                self.body = body
                self.method = method
        req = Request({'k': 'v'},
                      json.dumps(
                          {"subnetId": 1, "networkId": 2, "name": "name1"}),
                      "POST")
        self.assertEqual(
            status.HTTP_200_OK,
            self.cpv.post(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_port_list_view_fail(self,  mock_fun_name):
        mock_fun_name.return_value = "fun_name"
        op = OperatePort()
        op.list_port = mock.Mock({})

        class Request:
            def __init__(self, query_params, body, method):
                self.query_params = query_params
                self.body = body
                self.method = method
        req = Request({'k': 'v'},
                      json.dumps(
                          {"subnetId": 1, "networkId": 2, "name": "name1"}),
                      "POST")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.cpv.post(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperatePort, 'list_ports')
    def test_port_lists_view(self, mock_list_ports, mock_fun_name):
        mock_list_ports.return_value = {'ports': [
            {"vimName": "a", "vimId": 1},
            {"vimName": "b", "vimId": 2}]}
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_200_OK,
            self.cpv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_port_lists_view_fail(self,  mock_fun_name):
        op = OperatePort()
        op.list_port = mock.Mock([])
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.cpv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperatePort, 'list_port')
    def test_port_list_view2(self, mock_list_port, mock_fun_name):
        mock_list_port.return_value = {"vimName": "a", "vimId": 1},\
            {"vimName": "b", "vimId": 2}
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_200_OK,
            self.dpv.get(req, "vimid", "tenantid", "portid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_port_list_view_fail2(self,  mock_fun_name):
        on = OperatePort()
        on.list_port = mock.Mock([])
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.dpv.get(req, "vimid", "tenantid", "portid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperatePort, 'delete_port')
    def test_delete_port(self, mock_delete_port, mock_fun_name):
        mock_delete_port.return_value.return_value = {"name": "name1",
                                                      "id": 1}
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            self.dpv.delete(req, "vimid", "tenantid", "portid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_delete_port_fail(self, mock_fun_name):
        op = OperatePort()
        op.delete_port = mock.Mock()
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.dpv.delete(req, "vimid", "tenantid", "portid").status_code)
