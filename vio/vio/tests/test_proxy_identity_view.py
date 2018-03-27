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

from vio.pub.msapi import extsys
from vio.swagger.views.proxyplugin.httpclient import BaseClient
from vio.swagger.views.proxyplugin.identity import views


class TestIdentityServer(unittest.TestCase):

    def setUp(self):
        self.view = views.IdentityServer()

    @mock.patch.object(BaseClient, "buildRequest")
    @mock.patch.object(BaseClient, "_request")
    def test_get(self, mock_req, mock_build):
        mock_build.return_value = ("http://onap.org", {}, None)
        self.view.get(mock.Mock(), "openstack_regionone")
        mock_req.assert_called_once()

    @mock.patch.object(BaseClient, "send")
    def test_patch(self, mock_send):
        self.view.patch(mock.Mock(), "openstack_regionone", None)
        mock_send.assert_called_once()

    @mock.patch.object(BaseClient, "send")
    def test_post(self, mock_send):
        self.view.post(mock.Mock(), "openstack_regionone", None)
        mock_send.assert_called_once()

    @mock.patch.object(BaseClient, "send")
    def test_delete(self, mock_send):
        self.view.delete(mock.Mock(), "openstack_regionone", None)
        mock_send.assert_called_once()

    @mock.patch.object(BaseClient, "send")
    def test_head(self, mock_send):
        self.view.head(mock.Mock(), "openstack_regionone", None)
        mock_send.assert_called_once()


class TestTokenView(unittest.TestCase):

    def setUp(self):
        self.view = views.TokenView()

    @mock.patch("requests.get")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get_v3(self, mock_getvim, mock_req):
        req = mock.Mock()
        req.get_full_path.return_value = "identity/v3"
        res = mock.Mock()
        res.status_code = 200
        res.json.return_value = {
            "version": {
                "links": [{
                    "href": ""
                }]
            }
        }
        mock_req.return_value = res
        resp = self.view.get(req, "vmware_nova")
        self.assertEqual(resp.status_code, 200)
