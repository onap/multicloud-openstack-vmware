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
import requests
import unittest

from vio.swagger.views.fakeplugin.execute import views


class TestFakeExecute(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeExecute()

    @mock.patch.object(requests, "request")
    def test_gexecute_get(self, mock_req):
        req = mock.Mock()
        req.body = """{
            "method": "get",
            "url": "http://example.org"
        }
        """
        resp = mock.Mock()
        resp.json.return_value = {}
        resp.headers = {"Content-Type": "application/json"}
        resp.status_code = 200
        mock_req.return_value = resp
        resp = self.view.post(req)
        self.assertEqual(200, resp.status_code)
