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

from vio.vsphere import utils
from vio.vsphere import ovf

from pyVmomi import vim
# from pyVmomi.vim.vm.device import VirtualEthernetCard
from pyVim import connect
import paramiko

import os
# import yaml
import requests


def new_vc():
    host = os.getenv("VSPHERE_HOST")
    username = os.getenv("VSPHERE_USER")
    password = os.getenv("VSPHERE_PASS")
    nvc = VCenter(host, username, password)
    return nvc


def new_esxi():
    host = os.getenv("ESXI_HOST")
    username = os.getenv("ESXI_USER")
    password = os.getenv("ESXI_PASS")
    nesxi = Esxi(host, username, password)
    return nesxi


class Esxi(object):
    def __init__(self, host=None, username=None, password=None):
        if not (host and username and password):
            raise Exception("host or username or password not specified")
        self.host = host
        self.username = username
        self.password = password
        self.ssh = self.get_ssh_session()

    def get_ssh_session(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, username=self.username, password=self.password)
        return ssh

    def exec_cmd(self, cmd):
        ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command(cmd)
        # import ipdb; ipdb.set_trace()
        return {
            "stdin": ssh_stdin.read() if ssh_stdin.readable() else "",
            "stdout": ssh_stdout.read() if ssh_stdout.readable() else "",
            "stderr": ssh_stderr.read() if ssh_stderr.readable() else "",
        }

    def flat_vmdk(self, datastore, vmdk):
        target_vmdk = vmdk.rstrip(".vmdk") + "-new.vmdk"
        print("Extending %s to %s" % (vmdk, target_vmdk))
        vmdk_path = "/vmfs/volumes/%s/%s" % (datastore, vmdk)
        target_path = "/vmfs/volumes/%s/%s" % (datastore, target_vmdk)
        cmd = "vmkfstools -i %s %s" % (vmdk_path, target_path)
        output = self.exec_cmd(cmd)
        if output["stderr"]:
            raise Exception(output["stderr"])
        output["target_vmdk"] = target_vmdk
        return output


class VCenter(object):
    def __init__(self, host=None, username=None, password=None):
        if not (host and username and password):
            raise Exception("host or username or password not specified")
        self.host = host
        self.username = username
        self.password = password
        self.datacenter = ""
        self.cluster = ""
        self.datastore = ""
        self.insecure = True
        self.service_instance = connect.SmartConnectNoSSL(
                host=self.host, user=self.username, pwd=self.password)
        self.vcontent = self.service_instance.RetrieveContent()
        # self.GetClient()

    def clone_vm(self, src, dst, power_on=False, wait=True):
        pass

    def wait_for_task(self, task):
        """ wait for a vCenter task to finish """
        task_done = False
        while not task_done:
            if task.info.state == 'success':
                return task.info.result
            if task.info.state == 'error':
                raise Exception(task.info.error.msg)
                # print("there was an error")
                # task_done = True

    def find_datastore(self, ds_name):
        datacenters_object_view = \
            self.vcontent.viewManager.CreateContainerView(
                self.vcontent.rootFolder,
                [vim.Datacenter],
                True)
        datacenter = None
        datastore = None
        for dc in datacenters_object_view.view:
            datastores_object_view = \
                self.vcontent.viewManager.CreateContainerView(
                    dc,
                    [vim.Datastore],
                    True)
            for ds in datastores_object_view.view:
                if ds.info.name == ds_name:
                    datacenter = dc
                    datastore = ds
                    return datacenter, datastore
        return datacenter, datastore

    def upload_file(self, filepath, datastore, folder="onap-test"):
        if not os.path.exists(filepath):
            raise Exception("%s not exists" % filepath)
        print("Getting datastore %s" % datastore)
        dc, ds = self.find_datastore(datastore)
        files = [filepath, filepath.rstrip(".vmdk")+"-flat.vmdk"]
        upload_count = 0
        for fp in files:
            if not os.path.exists(fp):
                continue
            upload_count += 1
            file_name = fp.split("/")[-1]
            remote_file = "/" + folder + "/" + file_name
            resource = "/folder" + remote_file
            params = {"dsName": ds.info.name,
                      "dcPath": dc.name}
            http_url = "https://" + self.host + ":443" + resource
            # print(http_url)
            # si, vconetnt = self.GetClient()
            # get cookies
            client_cookie = self.service_instance._stub.cookie
            cookie_name = client_cookie.split("=", 1)[0]
            cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
            cookie_path = client_cookie.split("=", 1)[1].split(
                ";", 1)[1].split(";", 1)[0].lstrip()
            cookie_text = " " + cookie_value + "; $" + cookie_path
            # Make a cookie
            cookie = dict()
            cookie[cookie_name] = cookie_text

            # Get the request headers set up
            headers = {'Content-Type': 'application/octet-stream'}

            with open(fp, "rb") as f:
                # Connect and upload the file
                print("Uploading file %s" % filepath)
                resp = requests.put(http_url,
                                    params=params,
                                    data=f,
                                    #    files={"file": f},
                                    headers=headers,
                                    cookies=cookie,
                                    verify=False)
                # import ipdb; ipdb.set_trace()
                if resp.status_code not in [200, 201]:
                    raise Exception("failed to upload %s to %s: %s" % (
                        filepath, datastore, resp.content))
                print(resp)
        print("upload success")
        return upload_count

    def deploy_ovf(self, vmdk_path, ovf_path=None, datacenter=None,
                   cluster=None, datastore=None):
        if not datacenter and not self.datacenter:
            raise Exception("not set datacenter")
        if not cluster and not self.cluster:
            raise Exception("not set cluster")
        if not datastore and not self.datastore:
            raise Exception("not set datastore")
        # if not ovf_path:
        #     raise Exception("not set ovf_path")
        ovf.deploy_ovf(self.service_instance, vmdk_path, ovf_path,
                       datacenter, cluster, datastore)
        print("Deploy success.")

    def deploy_ova(self, ova_path, datacenter=None, cluster=None,
                   datastore=None):
        pass

    def validate_image(self, vmdk_path, vm_name):
        # import ipdb; ipdb.set_trace()
        print("finding vm %s" % vm_name)
        vmdk_name = vmdk_path.split("/")[-1]
        vm = self.find_vm(vm_name)
        dc = vm.datacenter
        cluster = vm.cluster
        ds = vm.status()['datastores'][0]
        # vmdk_name = filepath.split("/")[-1]
        print("uploading vmdk file %s" % vmdk_name)
        ovf.deploy_ovf(self.service_instance, vmdk_path, ovf_path=None,
                       datacenter=dc.name, cluster=cluster.name,
                       datastore=ds.name)
        tmp_vm = self.find_vm("vmtest-template")
        print("attaching disk to vm %s" % vm_name)
        # dsfilepath = "[%s] %s/%s" % (
        # ds.name, "vmtest-template", "vmdisk1.vmdk")
        dsfilepath = tmp_vm.disks()[0].backing.fileName
        print("dsfilepath=%s" % dsfilepath)
        vm.add_disk(filepath=dsfilepath)
        print("power on vm %s" % vm_name)
        ret = vm.power_on()
        if ret is not None:
            raise Exception("error to poweron vm: %s", ret)
        print("power off vm %s" % vm_name)
        vm.power_off()
        print("Cleaning")
        vm.remove_disk("Hard disk 2", retain_file=True)
        tmp_vm.delete()

    def find_ds(self, ds_name):
        ds = utils.get_obj(self.vcontent, [vim.Datastore], ds_name)
        return ds

    def find_dc(self, dc_name):
        dc = utils.get_obj(self.vcontent, [vim.Datacenter], dc_name)
        return dc

    # def find_cluster(self, cluster):
    #     cluster = utils.get_obj(self.vcontent, [vim.C], name)

    def find_vm(self, vm_name):
        return VM(self, vm_name)


class VM(object):
    def __init__(self, vc, name):
        self.vc = vc
        vm = utils.get_obj(self.vc.vcontent, [vim.VirtualMachine], name)
        if vm is None:
            raise Exception("VM %s not found" % name)
        self.vm = vm
        self.name = name

    @property
    def datacenter(self):
        res = self.vm.resourcePool
        while True:
            if res is None:
                break
            if str(res).startswith("'vim.Datacenter"):
                return res
            res = res.parent
        return None

    @property
    def cluster(self):
        res = self.vm.resourcePool
        while True:
            if res is None:
                break
            if str(res).startswith("'vim.ClusterComputeResource"):
                return res
            res = res.parent
        return None

    def status(self):
        ret = {
            "name": self.vm.name,
            "resource_pool": self.vm.resourcePool,
            "cluster": self.cluster,
            "datacenter": self.datacenter,
            "datastores": [ds for ds in self.vm.datastore],
            "power_state": self.vm.runtime.powerState,
        }
        if self.vm.network:
            ret["networks"] = [net for net in self.vm.network]
        if self.vm.snapshot:
            ret["snapshots"] = [ss for ss in self.vm.snapshot]
        return ret

    @property
    def power_state(self):
        return self.vm.runtime.powerState

    def power_on(self):
        if self.power_state != "poweredOn":
            # task = self.vm.PowerOn()
            # print("power_on task:", task)
            # result = wait_for_task(task)
            # print("power_on result:", result)
            result = self.vc.wait_for_task(self.vm.PowerOn())
            return result

    def power_off(self):
        if self.power_state != "poweredOff":
            # task =  self.vm.PowerOff()
            # print("power_off task:", task)
            # result = wait_for_task(task)
            # print("power_off result:", result)
            result = self.vc.wait_for_task(self.vm.PowerOff())
            return result

    def delete(self):
        self.power_off()
        result = self.vc.wait_for_task(self.vm.Destroy())
        return result

    def clone(self, dst, wait=True):
        print("clone %s to %s" % (self.name, dst))
        relospec = vim.vm.RelocateSpec(pool=self.vm.resourcePool)
        clonespec = vim.vm.CloneSpec(location=relospec)
        clonespec.powerOn = False
        task = self.vm.Clone(name=dst, folder=self.vm.parent, spec=clonespec)
        print("clone task:", task)
        if wait:
            print("wait for task:", task)
            result = self.vc.wait_for_task(task)
            print("task result:", result)
            return VM(self.vc, result.name)
        return task

    def add_nic(self, network_name, nic_type="vmxnet3", mac=None):
        spec = vim.vm.ConfigSpec()
        nic_spec = vim.vm.device.VirtualDeviceSpec()
        nic_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add

        if nic_type == "e1000":
            nic_spec.device = vim.vm.device.VirtualE1000()
        elif nic_type == "e1000e":
            nic_spec.device = vim.vm.device.VirtualE1000e()
        elif nic_type == 'vmxnet':
            nic_spec.device = vim.vm.device.VirtualVmxnet()
        elif nic_type == 'vmxnet2':
            nic_spec.device = vim.vm.device.VirtualVmxnet2()
        elif nic_type == "vmxnet3":
            nic_spec.device = vim.vm.device.VirtualVmxnet3()
        else:
            raise Exception("not supported nic type %s" % nic_type)

        network = utils.get_obj(self.vc.vcontent, [vim.Network], network_name)
        VirtualEthernetCard = vim.vm.device.VirtualEthernetCard
        if isinstance(network, vim.OpaqueNetwork):
            nic_spec.device.backing = \
                VirtualEthernetCard.OpaqueNetworkBackingInfo()
            nic_spec.device.backing.opaqueNetworkType = \
                network.summary.opaqueNetworkType
            nic_spec.device.backing.opaqueNetworkId = \
                network.summary.opaqueNetworkId
        elif isinstance(network, vim.dvs.DistributedVirtualPortgroup):
            nic_spec.device.backing = \
                VirtualEthernetCard.DistributedVirtualPortBackingInfo()
            # nic_spec.device.backing.port = network
            nic_spec.device.backing.port = vim.dvs.PortConnection()
            # nic_spec.device.backing.port.portgroupKey = port.portgroupKey
            nic_spec.device.backing.port.portgroupKey = network.key
            nic_spec.device.backing.port.switchUuid = \
                network.config.distributedVirtualSwitch.uuid
            # nic_spec.device.backing.port.switchUuid = port.dvsUuid
            # nic_spec.device.backing.port.portKey = port.key
        else:
            nic_spec.device.backing = \
                VirtualEthernetCard.NetworkBackingInfo()
            nic_spec.device.backing.useAutoDetect = False
            # nic_spec.device.backing.network = network
            nic_spec.device.backing.deviceName = network

        nic_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        nic_spec.device.connectable.startConnected = True
        nic_spec.device.connectable.allowGuestControl = True
        nic_spec.device.connectable.connected = False
        nic_spec.device.connectable.status = 'untried'
        nic_spec.device.wakeOnLanEnabled = True
        nic_spec.device.addressType = 'assigned'
        if mac:
            nic_spec.device.macAddress = mac

        spec.deviceChange = [nic_spec]
        task = self.vm.ReconfigVM_Task(spec=spec)
        result = self.vc.wait_for_task(task)
        # result == None
        return result

    def remove_nics(self):
        nics = []
        for dev in self.vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualEthernetCard):
                nics.append(dev)
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = []
        for dev in nics:
            virtual_nic_spec = vim.vm.device.VirtualDeviceSpec()
            virtual_nic_spec.operation = \
                vim.vm.device.VirtualDeviceSpec.Operation.remove
            virtual_nic_spec.device = dev
            spec.deviceChange.append(virtual_nic_spec)
        task = self.vm.ReconfigVM_Task(spec=spec)
        result = self.vc.wait_for_task(task)
        # result == None
        return result

    def add_disk(self, disk_size=0, disk_type="thin", filepath=None,
                 wait=True):
        spec = vim.vm.ConfigSpec()
        unit_number = 0
        for dev in self.vm.config.hardware.device:
            if hasattr(dev.backing, 'fileName'):
                unit_number = int(dev.unitNumber) + 1
                # unit_number 7 reserved for scsi controller
                if unit_number == 7:
                    unit_number += 1
            if isinstance(dev, vim.vm.device.VirtualSCSIController):
                controller = dev
        dev_changes = []
        if disk_size <= 0 and not filepath:
            raise Exception("Neither disk_size nor filepath specified")
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        if not filepath:
            disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        if filepath:
            disk_spec.device.backing.fileName = filepath
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = unit_number
        if not filepath:
            new_disk_kb = int(disk_size) * 1024 * 1024
            disk_spec.device.capacityInKB = new_disk_kb
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        spec.deviceChange = dev_changes
        task = self.vm.ReconfigVM_Task(spec=spec)
        if disk_size:
            print("Adding a %sGB disk to vm %s" % (disk_size, self.name))
        else:
            print("Attaching %s disk to vm %s" % (filepath, self.name))
        if wait:
            ret = self.vc.wait_for_task(task)
            return ret
        return task

    def remove_disk(self, disk_label, retain_file=False, wait=True):
        print("Attempt to remove %s from %s" % (disk_label, self.name))
        virtual_hdd_device = None
        if isinstance(disk_label, int):
            if disk_label < 1:
                return {"error": (
                    "invalid disk index %d, disk "
                    "index starting from 1" % disk_label)
                    }
            count = 0
            for dev in self.vm.config.hardware.device:
                if isinstance(dev, vim.vm.device.VirtualDisk):
                    count += 1
                    if count == disk_label:
                        virtual_hdd_device = dev
        elif isinstance(disk_label, str):
            for dev in self.vm.config.hardware.device:
                if (isinstance(dev, vim.vm.device.VirtualDisk) and
                        dev.deviceInfo.label == disk_label):
                    virtual_hdd_device = dev
        if virtual_hdd_device is None:
            return {"error": "disk %s not found" % disk_label}
        virtual_hdd_spec = vim.vm.device.VirtualDeviceSpec()
        virtual_hdd_spec.operation = \
            vim.vm.device.VirtualDeviceSpec.Operation.remove
        if not retain_file:
            virtual_hdd_spec.fileOperation = \
                vim.vm.device.VirtualDeviceSpec.FileOperation.destroy
        virtual_hdd_spec.device = virtual_hdd_device
        spec = vim.vm.ConfigSpec()
        spec.deviceChange = [virtual_hdd_spec]
        task = self.vm.ReconfigVM_Task(spec=spec)
        if wait:
            ret = self.vc.wait_for_task(task)
            return ret
        return task

    def disks(self):
        disks = []
        for dev in self.vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualDisk):
                disks.append(dev)
        return disks
