# Copyright (c) 2019 VMware, Inc.
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

import mock
import unittest

from vio import heatbridge
from vio.pub.vim.vimapi.heat import OperateStack
from vio.pub.vim.vimapi.nova import OperateServers


class TestHeatBridge(unittest.TestCase):

    @mock.patch.object(OperateServers, "OperateServers")
    @mock.patch.object(OperateStack, "OperateStack")
    def test_heat_bridge(self, mock_stack, mock_server):
        stack_op = mock.Mock()
        stack_op.get_stack_resources.return_value = [mock.Mock(
            resource_type="OS::Nova::Server",
            status="CREATE_COMPLETE",
            physical_resource_id="server-id",
        )]
        mock_stack.return_value = stack_op
        server_op = mock.Mock()
        server = mock.Mock(
            name="server",
            id="server-id",
            status="ACTIVE",
            links=[{
                "rel": "self",
                "href": "/servers/server-id"
            }]
        )
        server_op.get_server.return_value = server
        mock_server.return_value = server_op
        vim_info = {
            "vimId": "vim-id",
            "name": "vmware_nova",
            "userName": "user",
            "password": "pass",
            "url": "http://1.2.3.4:5000"
        }
        ret = heatbridge.heat_bridge(vim_info, "stack-id")
        expect_ret = {
            "servers": [{
                "name": server.name,
                "id": server.id,
                "status": server.status,
                "link": "/servers/server-id"
            }]
        }
        self.assertEqual(ret, expect_ret)
