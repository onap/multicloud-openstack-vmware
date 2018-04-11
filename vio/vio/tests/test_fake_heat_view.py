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

from vio.swagger.views.fakeplugin.heat import views
from vio.swagger.views.fakeplugin.fakeData import fakeResponse

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00" \
        "TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
        "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4" \
        "bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"
STACK_ID = "3095aefc-09fb-4bc7-b1f0-f21a304e864c"
STACK_NAME = "simple_stack"


class TestFakeHeatResources(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeHeatResources()

    @mock.patch.object(fakeResponse, "getStackResource")
    def test_get_heat_resource(self, mock_getStackResource):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_getStackResource.return_value = {
            "stack": "1234abcd"
        }
        resp = self.view.get(req, "1234abcd", STACK_ID)
        self.assertEqual(200, resp.status_code)
