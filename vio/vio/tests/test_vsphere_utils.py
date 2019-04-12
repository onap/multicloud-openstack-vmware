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

import unittest
import mock

from vio.vsphere import utils

from pyVim import connect
from pyVmomi import vim


vsphere_conf = """
vsphere:
  host: localhost
  username: user
  password: pass
"""

vmdk_meta = """
version=1
CID=cid
parentCID=pcid
ddb.adapterType="lsilogic"
createType="streamOptimized"
ddb.virtualHWVersion="11"
ddb.thinProvisioned="true"
ddb.deletable="true"
ddb.longContentID="lcid"
RDONLY 20971520 SPARSE "call-me-stream.vmdk"
"""


class VsphereUtilsTest(unittest.TestCase):

    def test_get_obj(self):
        content = mock.Mock()
        mock_obj_a = mock.Mock()
        mock_obj_a.name = "a"
        mock_obj_b = mock.Mock()
        mock_obj_b.name = "b"
        content.viewManager.CreateContainerView.return_value = mock.Mock(
            view=[mock_obj_a, mock_obj_b]
        )
        obj = utils.get_obj(content, "server", "b")
        self.assertEqual(obj.name, "b")
        obj = utils.get_obj(content, "server", None)
        self.assertEqual(obj.name, "a")
        obj = utils.get_obj(content, "server", "c")
        self.assertIsNone(obj)

    def test_get_objs(self):
        mock_obj = mock.Mock()
        mock_obj.name = "a"
        content = mock.Mock()
        content.viewManager.CreateContainerView.return_value = mock.Mock(
            view=[mock_obj]
        )
        objs = utils.get_objs(content, "server")
        exp_objs = {
            "a": mock_obj
        }
        self.assertEqual(exp_objs, objs)

    def test_wait_for_task_success(self):
        task = mock.Mock()
        task.info.state = "success"
        task.info.result = "result"
        ret = utils.wait_for_task(task)
        self.assertEqual(ret, task.info.result)

    def test_wait_for_task_error(self):
        task = mock.Mock()
        task.info.state = "error"
        task.info.result = "result"
        ret = utils.wait_for_task(task)
        self.assertIsNone(ret)

    @mock.patch.object(connect, "SmartConnectNoSSL")
    @mock.patch.object(utils, "open")
    def test_get_client(self, mock_open, mock_conn):
        mock_open.return_value = vsphere_conf
        si = mock.Mock()
        si.RetrieveContent.return_value = "lalala"
        mock_conn.return_value = si
        ret = utils.GetClient()
        self.assertEqual(ret, "lalala")

    @mock.patch.object(vim, "vm")
    @mock.patch.object(utils, "get_obj")
    @mock.patch.object(utils, "GetClient")
    def test_clone_vm(self, mock_client, mock_getobj, mock_vm):
        client = mock.Mock()
        vm = mock.Mock()
        mock_client.return_value = client
        mock_getobj.return_value = vm
        mock_vm.RelocateSpec.return_value = {}
        mock_vm.CloneSpec.return_value = mock.Mock(power_on=False)
        task = mock.Mock()
        task.info.state = "success"
        task.info.result = "result"
        vm.Clone.return_value = task
        ret = utils.CloneVM("src", "dst")
        self.assertEqual(ret, task)

    @mock.patch.object(utils, "open")
    def test_read_vmdk_meta(self, mock_open):
        mock_file = mock.mock_open(read_data=vmdk_meta)
        mock_open.side_effect = [mock_file.return_value]
        exp_dict = {'CID': 'cid',
                    'adapterType': 'lsilogic',
                    'createType': 'streamOptimized',
                    'deletable': 'true',
                    'diskType': 'SPARSE',
                    'longContentID': 'lcid',
                    'parentCID': 'pcid',
                    'rwMode': 'RDONLY',
                    'size': '20971520',
                    'thinProvisioned': 'true',
                    'version': '1',
                    'virtualHWVersion': '11'}
        ret = utils.vmdk_metadata("aaaa")
        self.assertDictEqual(ret, exp_dict)
