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
from vio.swagger.views.volume import views
from vio.pub.vim.vimapi.cinder import OperateVolume


class TestGetDeleteVolumeView(unittest.TestCase):

    def setUp(self):
        self.view = views.GetDeleteVolumeView()

    @mock.patch.object(OperateVolume.OperateVolume, "get_vim_volume")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get(self, mock_getvim, mock_getvol):
        mock_getvim.return_value = {
            "tenant": "tenant-id"
        }
        vol = mock.Mock()
        vol.attachments = []
        vol.id = "vol-id"
        vol.name = "vol-name"
        vol.created_at = "create time"
        vol.status = "ok"
        vol.volume_type = "vmdk"
        vol.size = 1
        vol.availability_zone = "nova"
        mock_getvol.return_value = vol
        ret = self.view.get(mock.Mock(), "vmware_nova", "tenant1", "vol-1")
        self.assertEqual(200, ret.status_code)

    @mock.patch.object(OperateVolume.OperateVolume, "get_vim_volume")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_get_fail(self, mock_getvim, mock_getvol):
        mock_getvim.return_value = {
            "tenant": "tenant-id"
        }
        mock_getvol.side_effect = [Exception("error here")]
        ret = self.view.get(mock.Mock(), "vmware_nova", "tenant1", "vol-1")
        self.assertEqual(500, ret.status_code)
