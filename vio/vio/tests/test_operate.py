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

import unittest
from vio.pub.vim.vimapi.network.OperateSubnet import OperateSubnet
from vio.pub.vim.vimapi.network.OperateNetwork import OperateNetwork
from vio.pub.vim.vimapi.network.OperatePort import OperatePort


class OperateTest(unittest.TestCase):

    def tearDown(self):
        pass

    def test_operatenetwork(self):

        class Network:
            def __init__(self, status):
                self.status = status
        network = Network("ok")
        network.id = 1
        network.name = "name1"
        network.project_id = 2
        network.provider_segmentation_id = 3
        network.provider_network_type = 4
        network.provider_physical_network = 5
        network.is_shared = 6
        network.is_router_external = 7
        op = OperateNetwork()
        self.assertDictContainsSubset({"status": "ok"}, op._convert(network))

    def test_operatesubnet(self):
        class Subnet:
            def __init__(self, status):
                self.status = status
        subnet = Subnet("ok")
        subnet.id = 1
        subnet.network_id = 2
        subnet.name = "name1"
        subnet.allocation_pools = "pool1"
        subnet.gateway_ip = "0.0.0.0"
        subnet.dns_nameservers = "server1"
        subnet.ip_version = "1.0"
        subnet.is_dhcp_enabled = "true"
        subnet.host_routes = 1
        subnet.cidr = 1

        os = OperateSubnet()
        self.assertDictContainsSubset({"status": "ok"}, os._convert(subnet))

    def test_operateport(self):
        class Port:
            def __init__(self, status):
                self.status = status
        port = Port("ok")
        port.id = 1
        port.network_id = 1
        port.name = "name"
        port.binding_vnic_type = 1
        port.mac_address = "aa:aa:aa:aa:aa:aa"
        port.subnet_id = 2
        port.security_group_ids = 1
        port.fixed_ips = [{"subnet_id": 1}]

        op = OperatePort()
        self.assertDictContainsSubset({"status": "ok"}, op._convert(port))
