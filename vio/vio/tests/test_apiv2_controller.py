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

from keystoneauth1.identity import v2 as keystone_v2
from keystoneauth1.identity import v3 as keystone_v3

from vio.api_v2.api_router import controller_builder as cb
from vio.api_v2.api_router import v0_controller
from vio.pub.msapi import extsys


class TestAPIv2Controller(unittest.TestCase):

    @mock.patch.object(keystone_v2, "Password")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get_vim_session_v2(self, mock_getvim, mock_kv2):
        mock_getvim.return_value = {
            "url": "http://aa/v2",
            "userName": "admin",
            "password": "admin",
            "domain": "default"
        }
        mock_kv2.return_value = mock.Mock()
        cb._get_vim_auth_session("vmware_vio", "tenant1")

    @mock.patch.object(keystone_v3, "Password")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get_vim_session_v3(self, mock_getvim, mock_kv3):
        mock_getvim.return_value = {
            "url": "http://aa/v3",
            "userName": "admin",
            "password": "admin",
            "domain": "default"
        }
        mock_kv3.return_value = mock.Mock()
        cb._get_vim_auth_session("vmware_vio", "tenant1")

    def test_convert_default_val(self):
        self.assertEqual(None, cb._convert_default_value("None"))
        self.assertEqual(True, cb._convert_default_value("true"))
        self.assertEqual(False, cb._convert_default_value("false"))

    def test_property_exist(self):
        res = {
            "pp": "dd"
        }
        self.assertEqual(True, cb._property_exists(res, "pp", required=False))
        self.assertEqual(False, cb._property_exists(res, "dd", required=False))
        self.assertRaises(
            Exception, cb._property_exists, res, "dd", required=True)

    def test_insert_dynamic_controller(self):
        controller = v0_controller.V0_Controller()
        cb.insert_dynamic_controller(controller)
        self.assertEqual(True, hasattr(controller, "hosts"))
        self.assertEqual(True, hasattr(controller, "images"))
        self.assertEqual(True, hasattr(controller, "ports"))
        self.assertEqual(True, hasattr(controller, "networks"))
        self.assertEqual(True, hasattr(controller, "subnets"))
