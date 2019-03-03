from vmtest import utils

from pyVmomi import vim
from pyVmomi.vim.vm.device import VirtualEthernetCard


class VCenter(object):
    def __init__(self):
        self.vcontent = utils.GetClient()

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


class VM(VCenter):
    def __init__(self, name):
        super(VM, self).__init__()
        # self.vcontent = GetClient()
        vm = utils.get_obj(self.vcontent, [vim.VirtualMachine], name)
        if vm is None:
            raise Exception("VM %s not found" % name)
        self.vm = vm
        self.name = name

    def status(self):
        return {
            "name": self.vm.name,
            "resource_pool": self.vm.resourcePool.config.entity,
            "datastores": [ds for ds in self.vm.datastore],
            "networks": [net for net in self.vm.network],
            "snapshots": [ss for ss in self.vm.snapshots],
            "power_state": self.vm.runtime.powerState,
        }

    @property
    def power_state(self):
        return self.vm.runtime.powerState

    def power_on(self):
        if self.power_state != "poweredOn":
            # task = self.vm.PowerOn()
            # print("power_on task:", task)
            # result = wait_for_task(task)
            # print("power_on result:", result)
            result = self.wait_for_task(self.vm.PowerOn())
            return result

    def power_off(self):
        if self.power_state != "poweredOff":
            # task =  self.vm.PowerOff()
            # print("power_off task:", task)
            # result = wait_for_task(task)
            # print("power_off result:", result)
            result = self.wait_for_task(self.vm.PowerOff())
            return result

    def delete(self):
        self.power_off()
        result = self.wait_for_task(self.vm.Destroy())
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
            result = self.wait_for_task(task)
            print("task result:", result)
            return VM(result.name)
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

        network = utils.get_obj(self.vcontent, [vim.Network], network_name)
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
        result = self.wait_for_task(task)
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
        result = self.wait_for_task(task)
        # result == None
        return result

    def add_disk(self, disk_size, disk_type="thin", wait=True):
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
        new_disk_kb = int(disk_size) * 1024 * 1024
        disk_spec = vim.vm.device.VirtualDeviceSpec()
        disk_spec.fileOperation = "create"
        disk_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        disk_spec.device = vim.vm.device.VirtualDisk()
        disk_spec.device.backing = \
            vim.vm.device.VirtualDisk.FlatVer2BackingInfo()
        if disk_type == 'thin':
            disk_spec.device.backing.thinProvisioned = True
        disk_spec.device.backing.diskMode = 'persistent'
        disk_spec.device.unitNumber = unit_number
        disk_spec.device.capacityInKB = new_disk_kb
        disk_spec.device.controllerKey = controller.key
        dev_changes.append(disk_spec)
        spec.deviceChange = dev_changes
        task = self.vm.ReconfigVM_Task(spec=spec)
        print("Adding a %sGB disk to vm %s" % (disk_size, self.name))
        if wait:
            ret = self.wait_for_task(task)
            return ret
        return task

    def remove_disk(self, disk_label, retain_file=False, wait=True):
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
            ret = self.wait_for_task(task)
            return ret
        return task

    def disks(self):
        disks = []
        for dev in self.vm.config.hardware.device:
            if isinstance(dev, vim.vm.device.VirtualDisk):
                disks.append(dev)
        return disks
