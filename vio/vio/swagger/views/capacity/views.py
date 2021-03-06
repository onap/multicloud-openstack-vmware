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

import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.exceptions import VimDriverVioException
from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.nova import OperateHypervisor
from vio.pub.vim.vimapi.nova import OperateLimits
from vio.pub.vim.vimapi.nova import OperateNova

from cinderclient import client


logger = logging.getLogger(__name__)


class CapacityCheck(APIView):

    def _check_capacity(self, hypervisor, requirement):
        avail_vcpu = hypervisor.get("vcpus") - hypervisor.get("vcpus_used")
        avail_mem = (hypervisor.get("memory_size") - hypervisor.get(
            "memory_used"))/1024
        avail_disk = hypervisor.get("local_disk_size") - hypervisor.get(
            "local_disk_used")
        req_vcpu = requirement.get("vCPU")
        req_mem = requirement.get("Memory")
        req_disk = requirement.get("Storage")
        if avail_vcpu < req_vcpu:
            return False
        if avail_mem < req_mem:
            return False
        if avail_disk < req_disk:
            return False
        return True

    def _check_nova_limits(self, limits, requirement):
        avail_vcpu = (
            limits.absolute.total_cores - limits.absolute.total_cores_used)
        avail_mem = (
            limits.absolute.total_ram - limits.absolute.total_ram_used)/1024
        req_vcpu = requirement.get("vCPU")
        req_mem = requirement.get("Memory")
        if avail_vcpu >= 0 and avail_vcpu < req_vcpu:
            return False
        if avail_mem >= 0 and avail_mem < req_mem:
            return False
        return True

    def _check_cinder_limits(self, limits, requirement):
        absolute = limits['absolute']
        avail_disk = (absolute.get(
            "maxTotalVolumeGigabytes") - absolute.get("totalGigabytesUsed"))
        req_disk = requirement.get("Storage")
        if avail_disk < req_disk:
            return False
        return True

    def _post_handler(self, request, vimid):
        try:
            requirement = json.loads(request.body)
        except ValueError as ex:
            return {'error': str(ex),
                    "status_code": status.HTTP_400_BAD_REQUEST}
        try:
            vim_info = extsys.get_vim_by_id(vimid)
        except VimDriverVioException as e:
            return {'error': str(e), "status_code": e.status_code}
        auth_info = {
            "username": vim_info['userName'],
            "password": vim_info['password'],
            "url": vim_info['url'],
            "project_name": vim_info['tenant']
        }

        # check nova limits
        servers_op = OperateLimits.OperateLimits()
        try:
            nova_limits = servers_op.get_limits(auth_info, None)
        except Exception as e:
            logger.exception("get nova limits error %(e)s", {"e": e})
            return {'error': str(e), "status_code": e.status_code}
        if not self._check_nova_limits(nova_limits, requirement):
            return {'result': False, "status_code": status.HTTP_200_OK}
        # check cinder limits
        cinder = client.Client(
            "3", auth_info['username'], auth_info['password'],
            auth_info['project_name'], auth_info['url'], insecure=True)
        try:
            limits = cinder.limits.get().to_dict()
        except Exception as e:
            logger.exception("get cinder limits error %(e)s", {"e": e})
            return {'error': str(e), "status_code": e.status_code}
        if not self._check_cinder_limits(limits, requirement):
            return {'result': False, "status_code": status.HTTP_200_OK}
        # Get Availability zones info
        nova_op = OperateNova.OperateAZ()
        try:
            azs = nova_op.list_availability_zones(auth_info, details=True)
        except Exception as e:
            logger.exception("get availability_zones error %(e)s", {"e": e})
            return {'error': str(e), "status_code": e.status_code}
        availability_zones = []
        for az in azs:
            if az.name == "internal":
                continue
            availability_zones.append({
                "availability-zone-name": az.name,
                "hosts": az.hosts,
                "vCPUTotal": 0,
                "vCPUAvail": 0,
                "MemoryTotal": 0,
                "MemoryAvail": 0,
                "StorageTotal": 0,
                "StorageAvail": 0,
            })
        # check hypervisor resources
        hypervisor_op = OperateHypervisor.OperateHypervisor()
        try:
            hypervisors = hypervisor_op.list_hypervisors(auth_info)
        except Exception as e:
            logger.exception("get hypervisors error %(e)s", {"e": e})
            return {'error': str(e), "status_code": e.status_code}
        ret = {'result': False, "status_code": status.HTTP_200_OK}
        # import ipdb; ipdb.set_trace()
        for hypervisor in hypervisors:
            if hypervisor.status != "enabled":
                continue
            hyper = hypervisor_op.get_hypervisor(auth_info, hypervisor.id)
            hyper_dict = hyper.to_dict()
            for az in availability_zones:
                if az['hosts'].get(hyper_dict["service_details"]['host']):
                    az['vCPUTotal'] += hyper_dict["vcpus"]
                    az['vCPUAvail'] += hyper_dict["vcpus"] - hyper_dict[
                        "vcpus_used"]
                    az['MemoryTotal'] += hyper_dict["memory_size"]
                    az['MemoryAvail'] += hyper_dict["memory_free"]
                    az['StorageTotal'] += hyper_dict["local_disk_size"]
                    az['StorageAvail'] += hyper_dict["local_disk_free"]
            if self._check_capacity(hyper_dict, requirement):
                ret["result"] = True
        if ret["result"]:
            for az in availability_zones:
                del az["hosts"]
            ret["AZs"] = availability_zones
        return ret

    def post(self, request, vimid):
        ret = self._post_handler(request, vimid)
        status_code = ret["status_code"]
        del ret["status_code"]
        if ret.get("AZs"):
            del ret["AZs"]
        return Response(data=ret, status=status_code)


class CapacityCheckV1(CapacityCheck):
    def post(self, request, cloud_owner, cloud_region):
        # import ipdb; ipdb.set_trace()
        vimid = cloud_owner + "_" + cloud_region
        ret = self._post_handler(request, vimid)
        status_code = ret["status_code"]
        del ret["status_code"]
        return Response(data=ret, status=status_code)
