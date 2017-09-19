# Copyright (c) 2017 VMware, Inc.
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
from vio.swagger.views.flavor.views import FlavorsView, FlavorView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova.OperateFlavors import OperateFlavors
from vio.swagger import nova_utils

VIM_INFO = {'vimId': 1, 'name': 'name1', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class FlavorViewTest(unittest.TestCase):

    def setUp(self):
        self.fsv = FlavorsView()
        self.fv = FlavorView()

    def tearDown(self):
        pass

    @mock.patch.object(nova_utils, 'flavor_formatter')
    @mock.patch.object(OperateFlavors, 'find_flavor')
    @mock.patch.object(OperateFlavors, 'get_flavor')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_flavor_list_view_fail(self, mock_vim_info, mock_get_flavor,
                                   mock_find_flavor, mock_formatter):

        mock_vim_info.return_value = VIM_INFO

        class Request:
            def __init__(self, query_params, body, method):
                self.query_params = query_params
                self.body = body
                self.method = method
        req = Request({'k': 'v'},
                      json.dumps({'name': 'flavor-name', 'flavor_id': 1}),
                      "POST")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.fsv.post(req, "vimid", "tenantid").status_code)

    @mock.patch.object(nova_utils, 'flavor_formatter')
    @mock.patch.object(OperateFlavors, 'get_flavor')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_flavor_get_fail(self, mock_vim_info,
                             mock_get_flavor, mock_formatter):
        mock_vim_info.return_value = VIM_INFO

        mock_formatter.return_value = {"id": 1, "name": "nova"}

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.fv.get(req, "vimid", "tenantid", "flavorid").status_code)

    @mock.patch.object(nova_utils, 'flavor_formatter')
    @mock.patch.object(OperateFlavors, 'list_flavors')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_flavors_get_fail(self, mock_vim_info,
                              mock_flavors, mock_formatter):
        mock_vim_info.return_value = VIM_INFO

        class Flavor:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        f1 = Flavor(1, "f1")
        f2 = Flavor(2, "f2")
        flavors = [f1, f2]
        mock_flavors.return_value = flavors
        mock_formatter.return_value = flavors

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.fsv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(nova_utils, 'flavor_formatter')
    @mock.patch.object(OperateFlavors, 'get_flavor')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_flavor_get(self, mock_vim_info, mock_flavors, mock_formatter):
        mock_vim_info.return_value = VIM_INFO

        class Flavor:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        f1 = Flavor(1, "f1")
        f2 = Flavor(2, "f2")
        flavors = [f1, f2]
        mock_flavors.return_value = flavors
        mock_formatter.return_value = {"id": 1, "name": "nova"}

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_200_OK,
            self.fv.get(req, "vimid", "tenantid", "flavorid").status_code)

    @mock.patch.object(OperateFlavors, 'delete_flavor')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_flavor_delete_view(self, mock_vim_info, mock_delete_flavor):

        mock_vim_info.return_value = VIM_INFO

        class Flavor:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        f = Flavor(1, "f1")

        mock_delete_flavor.return_value = f

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            self.fv.delete(req, "vimid", "tenantid", "flavorid").status_code)

    @mock.patch.object(OperateFlavors, 'delete_flavor')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_flavor_delete_view_fail(self, mock_vim_info, mock_delete_flavor):

        mock_vim_info.return_value = VIM_INFO
        mock_delete_flavor.side_effect = TypeError("wrong type")

        class Request:
            def __init__(self, query_params, method):
                self.query_params = query_params
                self.method = method
        req = Request({'k': 'v'}, "DELETE")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.fv.delete(req, "vimid", "tenantid", "flavorid").status_code)
