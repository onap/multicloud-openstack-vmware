from pyVim import connect
from pyVmomi import vim

import os
# import json
import yaml

vcontent = None


def get_obj(content, vimtype, name):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    return obj


def get_objs(content, vimtype):
    """
    Get all the vsphere objects associated with a given type
    """
    obj = {}
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        obj.update({c: c.name})
    return obj


def wait_for_task(task):
    """ wait for a vCenter task to finish """
    task_done = False
    while not task_done:
        if task.info.state == 'success':
            return task.info.result

        if task.info.state == 'error':
            print("there was an error")
            task_done = True


def GetClient():
    global vcontent
    if vcontent is not None:
        return vcontent
    vsphere_conf_path = os.getenv("VSPHERE_CONF", "/opt/etc/vsphere.yml")
    vsphere_conf = yaml.load(open(vsphere_conf_path, "r"))['vsphere']
    # vsphere_conf = json.load(open(vsphere_conf_path, "r"))['vsphere']
    host = vsphere_conf['host']
    username = vsphere_conf['username']
    password = vsphere_conf['password']
    insecure = vsphere_conf.get("insecure", True)
    if insecure:
        service_instance = connect.SmartConnectNoSSL(
            host=host, user=username, pwd=password)
    else:
        service_instance = connect.SmartConnect(
            host=host, user=username, pwd=password, port=443)
    vcontent = service_instance.RetrieveContent()
    return vcontent


def CloneVM(src, dst, power_on=False, wait=True):
    assert src != dst
    vcontent = GetClient()
    vm = get_obj(vcontent, [vim.VirtualMachine], src)
    print("src vm:", vm)
    relospec = vim.vm.RelocateSpec(pool=vm.resourcePool)
    clonespec = vim.vm.CloneSpec(location=relospec)
    clonespec.powerOn = power_on
    task = vm.Clone(name=dst, folder=vm.parent, spec=clonespec)
    print("clone task:", task)
    if wait:
        print("wait for task:", task)
        result = wait_for_task(task)
        print("task result:", result)
    return task


def DeployOVA(src, datacenter, resource_pool, datastore):
    pass
