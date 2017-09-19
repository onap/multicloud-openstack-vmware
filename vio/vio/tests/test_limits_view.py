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
# import json
import mock
from rest_framework import status
from vio.swagger.views.limits.views import LimitsView


from vio.pub.msapi import extsys
from vio.swagger import nova_utils
from vio.pub.vim.vimapi.nova.OperateLimits import OperateLimits

VIM_INFO = {'vimId': 1, 'name': 'name1', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class LimitsViewTest(unittest.TestCase):

    def setUp(self):
        self.lv = LimitsView()

    def tearDown(self):
        pass

    @mock.patch.object(nova_utils, 'server_limits_formatter')
    @mock.patch.object(OperateLimits, 'get_limits')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_server_get_limit(self, mock_vim_info,
                              mock_limits, mock_formatter):
        mock_vim_info.return_value = VIM_INFO
        mock_limits.return_value = {"name": "name1", "project_id": 1}
        mock_formatter.return_value = {"name": "name1", "project_id": 1}

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_200_OK,
            self.lv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(nova_utils, 'server_limits_formatter')
    @mock.patch.object(OperateLimits, 'get_limits')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_server_get_limit_fail(self, mock_vim_info,
                                   mock_limits, mock_formatter):
        mock_vim_info.return_value = VIM_INFO
        mock_limits.side_effect = KeyError('wrong type')
        mock_formatter.return_value = {"name": "name1", "project_id": 1}

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.lv.get(req, "vimid", "tenantid").status_code)
