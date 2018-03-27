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
from vio.swagger.views.image import views
from vio.pub.vim.vimapi.glance import OperateImage


class TestGetDeleteImageView(unittest.TestCase):

    def setUp(self):
        self.view = views.GetDeleteImageView()

    @mock.patch.object(OperateImage.OperateImage, "get_vim_image")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get(self, mock_getvim, mock_getimg):
        mock_getvim.return_value = {
            "tenant": "tenant-id"
        }
        img = mock.Mock()
        img.to_dict.return_value = {
            "id": "image-id"
        }
        mock_getimg.return_value = img
        resp = self.view.get(mock.Mock(), "vmware_nova", "tenant1", "image1")
        self.assertEqual(200, resp.status_code)
        self.assertEqual("image-id", resp.data.get('id'))
