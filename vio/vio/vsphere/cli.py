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

import fire

from vio.vsphere import utils
from vio.vsphere import vc


class Cli(object):
    def __init__(self):
        pass

    def connectcheck(self):
        utils.GetClient()
        print("Connection check success!")

    def clonevm(self, src, dst, poweron=False):
        nvc = vc.new_vc()
        src_vm = nvc.find_vm(src)
        # src_vm = vc.VM(src)
        dst_vm = src_vm.clone(dst)
        if poweron:
            dst_vm.power_on()
        # utils.CloneVM(src, dst)

    def delvm(self, name):
        nvc = vc.new_vc()
        vm = nvc.find_vm(name)
        vm.delete()
        print("VM %s deleted" % name)

    def addnic(self, vm_name, network):
        nvc = vc.new_vc()
        vm = nvc.find_vm(vm_name)
        vm.add_nic(network)
        print("Attach %s to network %s" % (vm_name, network))

    def delnics(self, vm_name):
        nvc = vc.new_vc()
        vm = nvc.find_vm(vm_name)
        vm.remove_nics()
        print("Deleted all nics of %s" % vm_name)

    def adddisk(self, vm_name, disk_size, disk_type="thin"):
        nvc = vc.new_vc()
        vm = nvc.find_vm(vm_name)
        ret = vm.add_disk(disk_size, disk_type=disk_type)
        print("Add %sGB disk to vm %s result: %s" % (disk_size, vm_name, ret))

    def attachdisk(self, vm_name, ds_name, vmdk_name):
        filepath = "[%s] %s" % (ds_name, vmdk_name)
        nvc = vc.new_vc()
        vm = nvc.find_vm(vm_name)
        ret = vm.add_disk(filepath=filepath)
        print("Attach %s to vm %s result: %s" % (filepath, vm_name, ret))

    def deldisk(self, vm_name, disk_label, retain=False):
        nvc = vc.new_vc()
        vm = nvc.find_vm(vm_name)
        try:
            disk_label = int(disk_label)
        except ValueError:
            pass
        ret = vm.remove_disk(disk_label, retain_file=retain)
        print("Del disk %s from vm %s result: %s" % (
            disk_label, vm_name, ret))

    def vmdk_meta(self, vmdk_path):
        meta = utils.vmdk_metadata(vmdk_path)
        print(meta)

    def deploy_ovf(self, vmdk_path, ovf_path=None, datacenter=None,
                   cluster=None, datastore=None):
        nvc = vc.new_vc()
        nvc.deploy_ovf(vmdk_path, ovf_path, datacenter, cluster, datastore)

    def upload_file(self, filepath, datastore, folder="onap-test"):
        nvc = vc.new_vc()
        nvc.upload_file(filepath, datastore, folder=folder)

    # def validate_image(self, filepath, vm_name, ds_name, folder="onap-test"):
    #     nvc = vc.new_vc()
    #     nvc.validate_image(filepath, vm_name, ds_name, folder=folder)

    def validate_image(self, filepath, vm_name):
        nvc = vc.new_vc()
        nvc.validate_image(filepath, vm_name)

    def test(self):
        # import ipdb; ipdb.set_trace()
        nvc = vc.new_vc()
        nvm = nvc.find_vm("el-cw")
        # import ipdb; ipdb.set_trace()
        print(nvm.status())


if __name__ == "__main__":
    fire.Fire(Cli)
