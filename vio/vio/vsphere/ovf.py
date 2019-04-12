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

from os import path
# from sys import exit
from threading import Thread
from time import sleep
# from argparse import ArgumentParser
# from getpass import getpass
import requests

# from pyVim import connect
from pyVmomi import vim
# from pyVmomi.VmomiSupport import long

from vio.vsphere import utils


def get_ovf_descriptor(ovf_path):
    """
    Read in the OVF descriptor.
    """
    if path.exists(ovf_path):
        with open(ovf_path, 'r') as f:
            try:
                ovfd = f.read()
                f.close()
                return ovfd
            except Exception as ex:
                raise Exception("Could not read file %s: %s" % (
                    ovf_path, str(ex)))


def get_obj_in_list(obj_name, obj_list):
    """
    Gets an object out of a list (obj_list) whos name matches obj_name.
    """
    for o in obj_list:
        if o.name == obj_name:
            return o
    raise Exception("Unable to find object by the name of %s in list:%s" %
                    (o.name, map(lambda o: o.name, obj_list)))


def get_objects(si, datacenter_name=None, datastore_name=None,
                cluster_name=None):
    """
    Return a dict containing the necessary objects for deployment.
    """
    # Get datacenter object.
    datacenter_list = si.content.rootFolder.childEntity
    if datacenter_name:
        datacenter_obj = get_obj_in_list(datacenter_name, datacenter_list)
    else:
        datacenter_obj = datacenter_list[0]

    # Get datastore object.
    datastore_list = datacenter_obj.datastoreFolder.childEntity
    if datastore_name:
        datastore_obj = get_obj_in_list(datastore_name, datastore_list)
    elif len(datastore_list) > 0:
        datastore_obj = datastore_list[0]
    else:
        print("No datastores found in DC (%s)." % datacenter_obj.name)

    # Get cluster object.
    cluster_list = datacenter_obj.hostFolder.childEntity
    if cluster_name:
        cluster_obj = get_obj_in_list(cluster_name, cluster_list)
    elif len(cluster_list) > 0:
        cluster_obj = cluster_list[0]
    else:
        print("No clusters found in DC (%s)." % datacenter_obj.name)

    # Generate resource pool.
    resource_pool_obj = cluster_obj.resourcePool

    return {"datacenter": datacenter_obj,
            "datastore": datastore_obj,
            "resource pool": resource_pool_obj}


def keep_lease_alive(lease):
    """
    Keeps the lease alive while POSTing the VMDK.
    """
    while(True):
        sleep(5)
        try:
            # Choosing arbitrary percentage to keep the lease alive.
            lease.HttpNfcLeaseProgress(50)
            if (lease.state == vim.HttpNfcLease.State.done):
                return
            # If the lease is released, we get an exception.
            # Returning to kill the thread.
        except Exception:
            return


def deploy_ovf(si, vmdk_path, ovf_path, datacenter, cluster, datastore):
    default_ovf = False
    if ovf_path is None:
        default_ovf = True
        cpath = path.dirname(path.realpath(__file__))
        ovf_path = cpath + "/templates/template.ovf"
    # import ipdb; ipdb.set_trace()
    vmdk_meta = utils.vmdk_metadata(vmdk_path)
    # vmdk_size = path.getsize(vmdk_path)
    ovfd = get_ovf_descriptor(ovf_path)
    objs = get_objects(si, datacenter, datastore, cluster)
    manager = si.content.ovfManager
    spec_params = vim.OvfManager.CreateImportSpecParams()
    print("Creating import ovf spec")
    import_spec = manager.CreateImportSpec(ovfd,
                                           objs["resource pool"],
                                           objs["datastore"],
                                           spec_params)
    if default_ovf:
        import_spec.importSpec.configSpec.deviceChange[
            1].device.capacityInKB = long(vmdk_meta['size'])
    lease = objs["resource pool"].ImportVApp(import_spec.importSpec,
                                             objs["datacenter"].vmFolder)
    while(True):
        if (lease.state == vim.HttpNfcLease.State.ready):
            # Assuming single VMDK.
            # url = lease.info.deviceUrl[0].url.replace('*', host)
            url = lease.info.deviceUrl[0].url
            # Spawn a dawmon thread to keep the lease active while POSTing
            # VMDK.
            keepalive_thread = Thread(target=keep_lease_alive, args=(lease,))
            keepalive_thread.start()
            print("Uploading %s to %s" % (vmdk_path, url))
            # POST the VMDK to the host via curl. Requests library would work
            # too.
            # curl_cmd = (
            #     "curl -Ss -X POST --insecure -T %s -H 'Content-Type: \
            #     application/x-vnd.vmware-streamVmdk' %s" %
            #     (vmdk_path, url))
            # system(curl_cmd)
            headers = {'Content-Type': 'application/x-vnd.vmware-streamVmdk'}
            client_cookie = si._stub.cookie
            cookie_name = client_cookie.split("=", 1)[0]
            cookie_value = client_cookie.split("=", 1)[1].split(";", 1)[0]
            cookie_path = client_cookie.split("=", 1)[1].split(
                ";", 1)[1].split(";", 1)[0].lstrip()
            cookie_text = " " + cookie_value + "; $" + cookie_path
            # Make a cookie
            cookie = dict()
            cookie[cookie_name] = cookie_text
            with open(vmdk_path, "rb") as f:
                resp = requests.post(url,
                                     # params=params,
                                     data=f,
                                     #    files={"file": f},
                                     headers=headers,
                                     cookies=cookie,
                                     verify=False)
                print("Upload results %s: %s" % (
                    resp.status_code, resp.content))
            lease.HttpNfcLeaseComplete()
            keepalive_thread.join()
            return
        elif (lease.state == vim.HttpNfcLease.State.error):
            raise Exception("Lease error: " + lease.error.msg)
