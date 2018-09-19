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

import mock
import unittest
import json

from vio.pub.msapi import extsys
from vio.swagger.views.workload import views
from vio.pub.vim.vimapi.heat import OperateStack


class TestGetDeleteStackView(unittest.TestCase):

    def setUp(self):
        self.view = views.GetDelStackViewV1()

    @mock.patch.object(OperateStack.OperateStack, "get_vim_stack")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get(self, mock_getvim, mock_getstk):
        mock_getvim.return_value = {}
        stk = mock.Mock(id="stack-id", status="CREATE_COMPLETE")
        # stk.to_dict.return_value = {
        #     "id": "stack-id"
        # }
        mock_getstk.return_value = stk
        resp = self.view.get(mock.Mock(), "vmware", "nova", "stack1")
        self.assertEqual(200, resp.status_code)
        self.assertEqual("stack-id", resp.data.get('workload_id'))
        self.assertEqual("CREATE_COMPLETE", resp.data.get('workload_status'))

    @mock.patch.object(OperateStack.OperateStack, "delete_vim_stack")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_delete(self, mock_getvim, mock_delstk):
        mock_getvim.return_value = {}
        resp = self.view.delete(
            mock.Mock(), "vmware", "nova", "stack1")
        self.assertEqual(204, resp.status_code)
        mock_delstk.assert_called_once()


class TestCreateStackView(unittest.TestCase):

    def setUp(self):
        self.view = views.CreateStackViewV1()

    @mock.patch.object(OperateStack.OperateStack, "create_vim_stack")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_post(self, mock_getvim, mock_createstk):
        mock_getvim.return_value = {
            "tenant": "tenant-id"
        }
        stk = mock.Mock()
        stk.id = "stack-id"
        mock_createstk.return_value = stk
        req = mock.Mock()
        req.body = json.dumps({
            "template_type": "heat",
            "template_data": {
                "parameters": {}
            }
        })
        resp = self.view.post(req, "vmware", "nova")
        self.assertEqual(201, resp.status_code)
        self.assertEqual("stack-id", resp.data["workload_id"])
