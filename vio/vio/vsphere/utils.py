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

from pyVim import connect
from pyVmomi import vim

import os
# import json
import yaml

vcontent = None
service_instance = None


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
        obj.update({c.name: c})
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
    # if  vcontent is not None:
    #     return vcontent
    global service_instance
    if vcontent is not None:
        return vcontent
    vsphere_conf_path = os.getenv("VSPHERE_CONF", "/opt/etc/vsphere.yml")
    vsphere_conf = yaml.safe_load(open(vsphere_conf_path, "r"))['vsphere']
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


def vmdk_metadata(vmdk_path):
    ret = {}
    with open(vmdk_path, "rb") as f:
        # import ipdb; ipdb.set_trace()
        for i in range(30):
            try:
                line = f.readline()
                if not line:
                    break
                text = line.decode()
                text = text.strip("\n")
                for k in ["version", "CID", "parentCID"]:
                    if text.startswith(k):
                        ret[k] = text.split("=")[-1]
                if text.startswith("ddb.adapterType"):
                    ret["adapterType"] = text.split('"')[1]
                elif text.startswith("createType"):
                    ret["createType"] = text.split('"')[1]
                elif text.startswith("ddb.virtualHWVersion"):
                    ret["virtualHWVersion"] = text.split('"')[1]
                elif text.startswith("ddb.thinProvisioned"):
                    ret["thinProvisioned"] = text.split('"')[1]
                elif text.startswith("ddb.deletable"):
                    ret["deletable"] = text.split('"')[1]
                elif text.startswith("ddb.longContentID"):
                    ret["longContentID"] = text.split('"')[1]
                elif text.startswith("R"):
                    splits = text.split(" ")
                    ret["rwMode"] = splits[0]
                    ret["size"] = splits[1]
                    ret["diskType"] = splits[2]
                # print(text)
                # print(ret)
            except UnicodeDecodeError:
                continue
            except Exception as ex:
                print(i, str(ex))
            # import ipdb; ipdb.set_trace()
    return ret
