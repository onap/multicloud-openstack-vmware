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

from vio.pub.utils import restcall


class TestAAIClient(unittest.TestCase):

    def setUp(self):
        self.view = restcall.AAIClient("vmware", "4.0")

    @mock.patch.object(restcall, "call_req")
    def test_get_vim(self, mock_call):
        mock_call.return_value = [0, '{"cloudOwner": "vmware"}']
        ret = self.view.get_vim(get_all=True)
        expect_ret = {"cloudOwner": "vmware"}
        self.assertEqual(expect_ret, ret)

    @mock.patch.object(restcall.AAIClient, "get_vim")
    @mock.patch.object(restcall, "call_req")
    def test_update_identity_url(self, mock_call, mock_getvim):
        mock_getvim.return_value = {}
        self.view.update_identity_url()
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_add_tenants(self, mock_call):
        tenants = {"tenants": [{"name": "admin", "id": "admin-id"}]}
        self.view.add_tenants(tenants)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_add_flavors(self, mock_call):
        flavors = {
            "flavors": [{
                "name": "m1.small",
                "id": "1",
                "vcpus": 1,
                "ram": 512,
                "disk": 10,
                "ephemeral": 0,
                "swap": 0,
                "is_public": True,
                "links": [{"href": "http://fake-url"}],
                "is_disabled": False
            }]
        }
        self.view.add_flavors(flavors)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_add_images(self, mock_call):
        images = {
            "images": [{
                "name": "ubuntu-16.04",
                "id": "image-id"
            }]
        }
        self.view.add_images(images)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_add_networks(self, mock_call):
        networks = {
            "networks": [{
                "name": "net-1",
                "id": "net-id",
                "segmentationId": 144
            }]
        }
        self.view.add_networks(networks)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_add_pservers(self, mock_call):
        pservers = {
            "hypervisors": [{
                "name": "compute-1",
                "vcpus": 100,
                "local_disk_size": 1000,
                "memory_size": 10240,
                "host_ip": "10.0.0.7",
                "id": "compute-1-id"
            }]
        }
        self.view.add_pservers(pservers)
        self.assertEqual(mock_call.call_count, 2)

    @mock.patch.object(restcall, "call_req")
    def test_del_tenants(self, mock_call):
        mock_call.return_value = [0]
        rsp = {
            "tenants": {
                "tenant": [{
                    "tenant-id": "tenant-id",
                    "resource-version": "version-1"
                }]
            }
        }
        self.view._del_tenants(rsp)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_del_flavors(self, mock_call):
        mock_call.return_value = [0]
        rsp = {
            "flavors": {
                "flavor": [{
                    "flavor-id": "fake-id",
                    "resource-version": "fake-version"
                }]
            }
        }
        self.view._del_flavors(rsp)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_del_images(self, mock_call):
        mock_call.return_value = [0]
        rsp = {
            "images": {
                "image": [{
                    "image-id": "fake-id",
                    "resource-version": "fake-version"
                }]
            }
        }
        self.view._del_images(rsp)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_del_networks(self, mock_call):
        mock_call.return_value = [0]
        rsp = {
            "oam-networks": {
                "oam-network": [{
                    "network-uuid": "fake-id",
                    "resource-version": "fake-version"
                }]
            }
        }
        self.view._del_networks(rsp)
        mock_call.assert_called_once()

    @mock.patch.object(restcall, "call_req")
    def test_del_azs(self, mock_call):
        mock_call.return_value = [0]
        rsp = {
            "availability-zones": {
                "availability-zone": [{
                    "availability-zone-name": "fake-name",
                    "resource-version": "fake-version"
                }]
            }
        }
        self.view._del_azs(rsp)
        mock_call.assert_called_once()