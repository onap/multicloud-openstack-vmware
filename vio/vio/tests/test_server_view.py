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
from vio.swagger.views.server.views import ListServersView, GetServerView


from vio.pub.msapi import extsys
from vio.swagger import nova_utils
from vio.pub.vim.vimapi.nova.OperateServers import OperateServers

VIM_INFO = {'vimId': 1, 'name': 'name1', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class ServerViewTest(unittest.TestCase):

    def setUp(self):
        self.lsv = ListServersView()
        self.gsv = GetServerView()

    def tearDown(self):
        pass

    @mock.patch.object(nova_utils, 'server_formatter')
    @mock.patch.object(OperateServers, 'list_server_interfaces')
    @mock.patch.object(OperateServers, 'list_servers')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_server_get(self, mock_vim_info, mock_servers,
                        mock_interfaces, mock_formatter):
        mock_vim_info.return_value = VIM_INFO

        class Server:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        s1 = Server(1, "s1")
        s2 = Server(2, "s2")
        servers = [s1, s2]
        mock_servers.return_value = servers
        mock_interfaces.return_value = servers
        mock_formatter.return_value = servers

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_200_OK,
            self.lsv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(nova_utils, 'server_formatter')
    @mock.patch.object(OperateServers, 'list_server_interfaces')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_server_get_fail(self, mock_vim_info,
                             mock_interfaces, mock_formatter):
        mock_vim_info.return_value = VIM_INFO

        class Server:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        s1 = Server(1, "s1")
        s2 = Server(2, "s2")
        servers = [s1, s2]
        os = OperateServers()
        os.list_servers = mock.Mock(return_value=[])
        mock_interfaces.return_value = servers
        mock_formatter.return_value = servers

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(status.HTTP_500_INTERNAL_SERVER_ERROR,
                         self.lsv.get(req, "vimid", "tenantid").status_code)

    @mock.patch.object(nova_utils, 'server_formatter')
    @mock.patch.object(OperateServers, 'list_servers')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_server_get_view_fail(self, mock_vim_info,
                                  mock_servers, mock_formatter):
        mock_vim_info.return_value = VIM_INFO

        class Server:
            def __init__(self, id, project_id, name, availability_zone):
                self.id = id
                self.project_id = project_id
                self.name = name
                self.availability_zone = availability_zone
        s1 = Server(1, "p1", "name1", "nova")
        s2 = Server(2, "p2", "name2", "nova")
        servers = [s1, s2]
        mock_servers.return_value = servers
        os = OperateServers()
        os.list_server_interfaces = mock.Mock(return_value=[])
        mock_formatter.return_value = servers

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.gsv.get(req, "vimid", "tenant", "serverid").status_code)

    @mock.patch.object(OperateServers, 'delete_server')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_delete_server_view(self, mock_vim_info, mock_delete_server):
        mock_vim_info.return_value = VIM_INFO

        class Project:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        p1 = Project(1, "p1")
        mock_delete_server.return_value = p1

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_204_NO_CONTENT,
            self.gsv.delete(req, "vimid", "tenantid", "serverid").status_code)

    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_delete_server_view_fail(self, mock_vim_info):
        mock_vim_info.return_value = VIM_INFO
        os = OperateServers()
        os.delete_server = mock.Mock(return_value=[])

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.gsv.delete(req, "vimid", "tenantid", "serverid").status_code)

    @mock.patch.object(nova_utils, 'server_formatter')
    @mock.patch.object(OperateServers, 'find_server')
    @mock.patch.object(OperateServers, 'get_server')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_server_post_fail(self, mock_vim_info, mock_get_servers,
                              mock_find_servers, mock_formatter):
        mock_vim_info.return_value = VIM_INFO
        mock_find_servers.return_value = {"id": 1, "name": "name1"}
        mock_get_servers.return_value = {"id": 1, "name": "name1"}
        mock_formatter.return_value = {"id": 1, "name": "name1"}

        class Request:
            def __init__(self, query_params, body, method):
                self.query_params = query_params
                self.body = body
                self.method = method
        req = Request({'k': 'v'},
                      json.dumps({"name": "abc", "networkId": 3,
                                  "cidr": 2, "ipVersion": 1}),
                      "POST")
        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.lsv.post(req, "vimid", "tenantid").status_code)
