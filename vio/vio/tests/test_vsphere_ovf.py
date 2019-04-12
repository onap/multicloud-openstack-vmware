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
import unittest
import os
import requests

from pyVmomi import vim

from vio.vsphere import utils, ovf


class VsphereOvfTest(unittest.TestCase):

    @mock.patch.object(os.path, "exists")
    @mock.patch.object(ovf, "open")
    def test_get_ovfd(self, mock_open, mock_path):
        mock_file = mock.mock_open(read_data="this is ovfd")
        mock_path.return_value = True
        mock_open.side_effect = [mock_file.return_value]
        ret = ovf.get_ovf_descriptor("/path/ovf")
        self.assertEqual(ret, "this is ovfd")

    def test_get_objs(self):
        dc = mock.Mock()
        dc.name = "datacenter"
        si = mock.Mock()
        si.content.rootFolder.childEntity = [dc]
        ds = mock.Mock()
        ds.name = "datastore"
        dc.datastoreFolder.childEntity = [ds]
        cs = mock.Mock()
        cs.name = "cluster"
        dc.hostFolder.childEntity = [cs]
        rp = mock.Mock()
        cs.resourcePool = rp
        exp_ret = {
            "datacenter": dc,
            "datastore": ds,
            "resource pool": rp
            }
        ret = ovf.get_objects(
            si, datacenter_name="datacenter", datastore_name="datastore",
            cluster_name=None)
        self.assertDictEqual(ret, exp_ret)

    @mock.patch.object(ovf, "sleep")
    @mock.patch.object(requests, "post")
    @mock.patch.object(ovf, "get_objects")
    @mock.patch.object(utils, "vmdk_metadata")
    @mock.patch.object(ovf, "open")
    def test_deploy_ovf(self, mock_open, mock_meta, mock_objs, mock_post,
                        mock_sleep):
        mock_file = mock.mock_open(read_data="vmdk file")
        mock_open.side_effect = [
            mock_file.return_value, mock_file.return_value]
        mock_meta.return_value = {"size": 1024}
        rp = mock.Mock()
        mock_objs.return_value = {
            "resource pool": rp,
            "datastore": mock.Mock(),
            "datacenter": mock.Mock(),
        }
        lease = mock.Mock()
        type(lease).state = mock.PropertyMock(side_effect=[
            vim.HttpNfcLease.State.ready, vim.HttpNfcLease.State.done])
        lease.info.deviceUrl = [mock.Mock(url="local")]
        rp.ImportVApp.return_value = lease
        resp = mock.Mock()
        resp.status_code = 200
        resp.content = "content"
        mock_post.return_value = resp
        si = mock.Mock()
        si._stub.cookie = "name=value;path"
        import_spec = mock.Mock()
        si.content.ovfManager.CreateImportSpec.return_value = import_spec
        device = mock.Mock()
        device.capacityInKB = 1
        import_spec.importSpec.configSpec.deviceChange = [device, device]
        ret = ovf.deploy_ovf(
            si, "path/vmdk", None, "datacenter", "cluster",
            "datastore")
        self.assertIsNone(ret)
