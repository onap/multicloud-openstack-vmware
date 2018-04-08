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

from vio.swagger.views.fakeplugin.image import views
from vio.swagger.views.fakeplugin.fakeData import fakeResponse


class TestFakeImageDetail(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeImageDetail()

    @mock.patch.object(fakeResponse, "image_detail")
    def test_get(self, mock_image_detail):
        mock_image_detail.return_value = {
            "id": "1234abcd"
        }
        resp = self.view.get(mock.Mock(), "1234abcd")
        self.assertEqual(200, resp.status_code)


class TestFakeImage(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeImage()

    @mock.patch.object(fakeResponse, "list_image")
    def test_get(self, mock_list_image):
        mock_list_image.return_value = {
            "images": [{"id": "1234abcd"}]
        }
        resp = self.view.get(mock.Mock())
        self.assertEqual(200, resp.status_code)


class TestFakeImageSchema(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeImageSchema()

    @mock.patch.object(fakeResponse, "image_schema")
    def test_get(self, mock_image_schema):
        mock_image_schema.return_value = {
            "name": "image"
        }
        resp = self.view.get(mock.Mock())
        self.assertEqual(200, resp.status_code)


class TestFakeImageVersion(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeImageVersion()

    @mock.patch.object(fakeResponse, "image_version")
    def test_get(self, mock_image_version):
        mock_image_version.return_value = {
            "versions": [{"id": "v1.0"}]
        }
        resp = self.view.get(mock.Mock())
        self.assertEqual(200, resp.status_code)


class TestFakeImageDownload(unittest.TestCase):

    def setUp(self):
        self.view = views.FakeImageDownload()

    @mock.patch.object(fakeResponse, "image_detail")
    def test_get(self, mock_image_version):
        mock_image_version.return_value = {
            "id": "1234abcd"
        }
        resp = self.view.get(mock.Mock(), "1234abcd")
        self.assertEqual(200, resp.status_code)
