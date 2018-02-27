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
from vio.swagger.views.network.views import CreateNetworkView
from vio.swagger.views.network.views import DeleteNetworkView

from vio.pub.utils import syscomm
from vio.pub.vim.vimapi.network.OperateNetwork import OperateNetwork


class NetworkViewTest(unittest.TestCase):

    def setUp(self):
        self.cnv = CreateNetworkView()
        self.dnv = DeleteNetworkView()

    def tearDown(self):
        pass

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateNetwork, 'list_networks')
    def test_network_lists_view(self, mock_list_networks, mock_fun_name):
        mock_list_networks.return_value = {'networks': [
            {"vimName": "name1", "vimId": 1},
            {"vimName": "name2", "vimId": 2}]}
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_200_OK,
            self.cnv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_network_lists_view_fail(self,  mock_fun_name):
        on = OperateNetwork()
        on.list_networks = mock.Mock([])
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.cnv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateNetwork, 'list_network')
    def test_network_list_view_fail(self, mock_list_network, mock_fun_name):

        mock_fun_name.return_value = "fun_name"
        mock_list_network.return_value = \
            {"vimName": "name", "vimId": 1, "returnCode": 0}

        class Request:
            def __init__(self, query_params, body, method):
                self.query_params = query_params
                self.body = body
                self.method = method
        req = Request({'k': 'v'},
                      json.dumps([{'name': 'net-name', 'id': 1}]),
                      "POST")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.cnv.post(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateNetwork, 'list_network')
    def test_network_list_view(self, mock_list_network, mock_fun_name):
        mock_list_network.return_value = {'networks': [
            {"vimName": "name1", "vimId": 1},
            {"vimName": "name2", "vimId": 2}]}
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_200_OK,
            self.dnv.get(req, "vimid", "tenantid", "networkid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_network_list_view_fail2(self,  mock_fun_name):
        on = OperateNetwork()
        on.list_network = mock.Mock([])
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.dnv.get(req, "vimid", "tenantid", "networkid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateNetwork, 'delete_network')
    def test_delete_network(self, mock_delete_network, mock_fun_name):
        mock_delete_network.return_value = {"name": "name1", "id": 1}
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            self.dnv.delete(req, "vimid", "tenantid", "networkid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_delete_network_fail(self, mock_fun_name):
        op = OperateNetwork()
        op.delete_network = mock.Mock()
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.dnv.delete(req, "vimid", "tenantid", "networkid").status_code)
