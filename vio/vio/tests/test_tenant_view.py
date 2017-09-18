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
import mock
from rest_framework import status
from vio.swagger.views.tenant.views import ListTenantsView


from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.keystone.OperateTenant import OperateTenant

VIM_INFO = {'vimId': 1, 'name': 'name1', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class TenantViewTest(unittest.TestCase):

    def setUp(self):
        self.lvt = ListTenantsView()

    def tearDown(self):
        pass

    @mock.patch.object(OperateTenant, 'get_projects')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_tenant_view(self, mock_vim_info, mock_projects):
        mock_vim_info.return_value = VIM_INFO

        class Project:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        p1 = Project(1, "p1")
        p2 = Project(2, "p2")
        projects = [p1, p2]
        mock_projects.return_value = projects

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'query': 'param'})
        self.assertEqual(
            status.HTTP_200_OK, self.lvt.get(req, "vimid").status_code)

    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_tenant_view_fail(self, mock_vim_info):
        mock_vim_info.return_value = VIM_INFO
        ot = OperateTenant()
        ot.get_projects = mock.Mock(return_value=[])

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'query': 'param'})
        self.assertEqual(
            self.lvt.get(req, "vimid").status_code,
            status.HTTP_500_INTERNAL_SERVER_ERROR)
