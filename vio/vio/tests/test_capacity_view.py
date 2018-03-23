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
from vio.pub.vim.vimapi.nova import OperateHypervisor
from vio.pub.vim.vimapi.nova import OperateLimits
from vio.swagger.views.capacity.views import CapacityCheck

from cinderclient import client


VIM_INFO = {'vimId': 1, 'name': 'openstack_regionone', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class CapacityCheckTest(unittest.TestCase):

    def setUp(self):
        self.view = CapacityCheck()

    @mock.patch.object(OperateHypervisor, "OperateHypervisor")
    @mock.patch.object(OperateLimits, "OperateLimits")
    @mock.patch.object(client, "Client")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_check_capacity_success(self, mock_get_vim, mock_cinder,
                                    mock_limit, mock_hypervisor):
        mock_get_vim.return_value = VIM_INFO
        req = mock.Mock()
        req.body = """{
            "vCPU": 1,
            "Memory": 1,
            "Storage": 500
        }"""
        oplimits = mock.Mock()
        absolute = mock.Mock(
            total_cores=20, total_cores_used=1,
            total_ram=128*1024, total_ram_used=4*1024)
        oplimits.get_limits.return_value = mock.Mock(absolute=absolute)
        mock_limit.return_value = oplimits

        climits = mock.Mock()
        climits.to_dict.return_value = {
            "absolute": {
                "maxTotalVolumeGigabytes": 5000,
                "totalGigabytesUsed": 100
            }
        }
        cclient = mock.Mock()
        cclient.limits.get.return_value = climits
        mock_cinder.return_value = cclient

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
        mock_hypervisor.return_value = ophypervisor
        resp = self.view.post(req, "openstack_regionone")
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual({"result": True}, resp.data)

    @mock.patch.object(OperateLimits, "OperateLimits")
    @mock.patch.object(extsys, "get_vim_by_id")
    def test_check_capacity_nova_limits_failed(
            self, mock_get_vim, mock_limit):
        mock_get_vim.return_value = VIM_INFO
        req = mock.Mock()
        req.body = """{
            "vCPU": 1,
            "Memory": 1,
            "Storage": 500
        }"""
        oplimits = mock.Mock()
        absolute = mock.Mock(
            total_cores=1, total_cores_used=1,
            total_ram=128*1024, total_ram_used=4*1024)
        oplimits.get_limits.return_value = mock.Mock(absolute=absolute)
        mock_limit.return_value = oplimits

        resp = self.view.post(req, "openstack_regionone")
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual({"result": False}, resp.data)

    def test_check_capacity_invalid_input(self):
        req = mock.Mock()
        req.body = "hello world"

        resp = self.view.post(req, "openstack_regionone")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
