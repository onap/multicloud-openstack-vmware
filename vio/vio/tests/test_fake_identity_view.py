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

from vio.swagger.views.fakeplugin.identity import views
from vio.swagger.views.fakeplugin.fakeData import fakeResponse

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00" \
        "TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
        "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4" \
        "bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"


class TestFakeProjects(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeProjects()

    @mock.patch.object(fakeResponse, "show_project")
    def test_get_project(self, mock_show_project):
        req = mock.Mock()
        req.META = {
            "HTTP_X_AUTH_TOKEN": Token
        }
        mock_show_project.return_value = {
            "stack": "1234abcd"
        }
        resp = self.view.get(req, "1234abcd")
        self.assertEqual(200, resp.status_code)


class TestFakeToken(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeToken()

    @mock.patch.object(fakeResponse, "keystone_version")
    def test_get_token(self, mock_keystone_version):
        mock_keystone_version.return_value = {
            "version": "v3"
        }
        resp = self.view.get(mock.Mock())
        self.assertEqual(200, resp.status_code)

    @mock.patch("requests.post")
    @mock.patch.object(fakeResponse, "keystone_token")
    def test_create_token(self, mock_keystone_token,  mock_post):
        req = mock.Mock()
        req.get_full_path.return_value = "identity/v3/auth/tokens"
        req.body = json.dumps(
            {"auth": {"scope": {"project": {"id": "1234abcd"}}}})
        mock_keystone_token.return_value = {
            "token": {"value": Token}}
        resp = self.view.post(req)
        self.assertEqual(201, resp.status_code)


class TestFakeTokenV2(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeTokenV2()

    @mock.patch.object(fakeResponse, "keystone_version2")
    def test_get_tokenV2(self, mock_keystone_version2):
        mock_keystone_version2.return_value = {
            "version": "v2"
        }
        resp = self.view.get(mock.Mock())
        self.assertEqual(200, resp.status_code)

    @mock.patch("requests.post")
    @mock.patch.object(fakeResponse, "keystone_tokenV2")
    def test_create_tokenV2(self, mock_keystone_tokenV2,  mock_post):
        req = mock.Mock()
        req.get_full_path.return_value = "identity/v2.0/tokens"
        req.body = json.dumps(
            {"auth": {"scope": {"project": {"id": "1234abcd"}}}})
        mock_keystone_tokenV2.return_value = {
            "token": {"value": Token}}
        resp = self.view.post(req)
        self.assertEqual(200, resp.status_code)


class TestFakeTenants(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeTenants()

    @mock.patch.object(fakeResponse, "get_tenants")
    def test_get_tanent(self, mock_get_tenants):
        mock_get_tenants.return_value = {
            "tenant": "1234abbcd"
        }
        resp = self.view.get(mock.Mock())
        self.assertEqual(200, resp.status_code)
