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
from vio.swagger.views.subnet.views import CreateSubnetView, DeleteSubnetView


from vio.pub.utils import syscomm
from vio.pub.vim.vimapi.network.OperateSubnet import OperateSubnet


class SubnetViewTest(unittest.TestCase):

    def setUp(self):
        self.csv = CreateSubnetView()
        self.dsv = DeleteSubnetView()

    def tearDown(self):
        pass

    @mock.patch.object(OperateSubnet, 'list_subnet')
    @mock.patch.object(syscomm, 'fun_name')
    def test_subnet_list_view(self, mock_list_port, mock_fun_name):

        # mock_fun_name = "fun_name"
        mock_list_port.return_value = {"vimName": "name", "vimId": 1,
                                       "tenantId": 1}

        class Request:
            def __init__(self, query_params, body, method):
                self.query_params = query_params
                self.body = body
                self.method = method
        req = Request({'k': 'v'},
                      json.dumps({"name": "name1", "networkId": 3,
                                  "cidr": 2, "ipVersion": 1}),
                      "POST")
        self.assertEqual(
            status.HTTP_200_OK,
            self.csv.post(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateSubnet, 'list_subnets')
    def test_subnet_lists_view(self, mock_list_subnets, mock_fun_name):

        class Subnet:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        s1 = Subnet(1, "s1")
        s2 = Subnet(2, "s2")
        subnets = [s1, s2]
        mock_list_subnets.return_value = subnets
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_200_OK,
            self.csv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_subnet_lists_view_fail(self, mock_fun_name):

        os = OperateSubnet()
        os.list_subnets = mock.Mock(return_value=[])

        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.csv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateSubnet, 'list_subnet')
    def test_subnet_get_view(self, mock_list_subnet, mock_fun_name):

        class Subnet:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        s = Subnet(1, "s1")

        mock_list_subnet.return_value = s
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_200_OK,
            self.dsv.get(req, "vimId", "tenantid", "subnetid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_subnet_get_view_fail(self, mock_fun_name):

        os = OperateSubnet()
        os.list_subnet = mock.Mock(return_value=[])

        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "GET")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.dsv.get(req, "vimid", "tenantid", "subnetid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    @mock.patch.object(OperateSubnet, 'delete_subnet')
    def test_subnet_delete_view(self, mock_delete_subnet, mock_fun_name):

        class Subnet:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        s = Subnet(1, "s1")

        mock_delete_subnet.return_value = s
        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            self.dsv.delete(req, "vimid", "tenantid", "subnetid").status_code)

    @mock.patch.object(syscomm, 'fun_name')
    def test_subnet_delete_view_fail(self, mock_fun_name):

        os = OperateSubnet()
        os.delete_subnet = mock.Mock(return_value=[])

        mock_fun_name.return_value = "fun_name"

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.dsv.delete(req, "vimid", "tenantid", "subnetid").status_code)
