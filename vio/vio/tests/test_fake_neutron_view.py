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

from vio.swagger.views.fakeplugin.neutron import views
from vio.swagger.views.fakeplugin.fakeData import fakeResponse

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00" \
        "TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
        "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4" \
        "bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"


class TestakeNeutron(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeNeutron()

    @mock.patch.object(fakeResponse, "neutron_version")
    def test_get_neutron_version(self, mock_neutron_version):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_neutron_version.return_value = {
            "version": "1.0"
        }
        resp = self.view.get(req)
        self.assertEqual(200, resp.status_code)
