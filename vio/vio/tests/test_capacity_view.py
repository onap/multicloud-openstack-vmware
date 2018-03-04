# Copyright (c) 2017-2018 VMware, Inc.
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

from rest_framework import status

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.keystone import OperateTenant
from vio.pub.vim.vimapi.nova import OperateHypervisor
from vio.swagger.views.capacity.views import CapacityCheck

VIM_INFO = {'vimId': 1, 'name': 'openstack_regionone', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class CapacityCheckTest(unittest.TestCase):

    def setUp(self):
        self.view = CapacityCheck()

    def tearDown(self):
        pass

    @mock.patch.object(OperateHypervisor, "OperateHypervisor")
    @mock.patch.object(OperateTenant, "OperateTenant")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_check_capacity_success(self, mock_get_vim, mock_tenant,
                                    mock_hypervisor):
        mock_get_vim.return_value = VIM_INFO
        req = mock.Mock()
        req.body = """{
            "vCPU": 1,
            "Memory": 1,
            "Storage": 500
        }"""
        optenant = mock.Mock()
        optenant.get_projects.return_value = [
            mock.Mock(id="fake_id", name="t1")]
        OperateTenant.return_value = optenant

        ophypervisor = mock.Mock()
        ophypervisor.list_hypervisors.return_value = [
            mock.Mock(id="compute01")]
        hyper = mock.Mock()
        hyper.to_dict.return_value = {
            "vcpus": 20,
            "vcpus_used": 1,
            "memory_size": 128*1024,
            "memory_used": 4*1024,
            "local_disk_size": 5000,
            "local_disk_used": 100
        }
        ophypervisor.get_hypervisor.return_value = hyper
        resp = self.view.post(req, "openstack_regionone")
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
