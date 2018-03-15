#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import pecan
from pecan import rest

from vio.api_v2.api_definition import utils


def _convert_vim_res_to_mc_res(vim_resource, res_properties):
    mc_resource = {}
    for key in res_properties:
        vim_res, attr = res_properties[key]["source"].split('.')
        action = res_properties[key].get("action", "copy")
        # TODO(xiaohhui): Actions should be in constants.
        if action == "copy":
            mc_resource[key] = vim_resource[vim_res][attr]

    return mc_resource


def _build_api_controller(api_meta):
    # Assume that only one path
    path, path_meta = api_meta['paths'].items()[0]
    # url path is behind third slash. The first is vimid, the second is
    # tenantid.
    path = path.split("/")[3]
    controller_name = path.upper() + "Controller"

    # Assume that only one resource
    name, resource_meta = api_meta['definitions'].items()[0]
    resource_properties = resource_meta['properties']

    controller_meta = {}
    if "get" in path_meta:
        # Add get method to controller.
        @pecan.expose("json")
        def _get(self, vim_id, tenant_id, resource_id):
            """ General GET """
            # TODO(xiaohhui): Get VIM resource from backend VIM by using
            # vim_path and stored authentication info.
            fake_vim_resource = {
                "hypervisor": {
                    "status": "enabled",
                    "service": {
                        "host": "compute01",
                        "disabled_reason": None,
                        "id": 7
                    },
                    "vcpus_used": 113,
                    "hypervisor_type": "VMware vCenter Server",
                    "local_gb_used": 1987,
                    "vcpus": 48,
                    "hypervisor_hostname": "domain-c202.22bfc05c-da55-4ba",
                    "memory_mb_used": 185538,
                    "memory_mb": 196516,
                    "current_workload": 0,
                    "state": "up",
                    "host_ip": "10.154.9.173",
                    "cpu_info": "",
                    "running_vms": 35,
                    "free_disk_gb": 4156,
                    "hypervisor_version": 6000000,
                    "disk_available_least": None,
                    "local_gb": 6143,
                    "free_ram_mb": 10978,
                    "id": 1
                }
            }

            mc_res = _convert_vim_res_to_mc_res(fake_vim_resource,
                                                resource_properties)
            return {"vimName": vim_id,
                    name: mc_res,
                    "tenantId": tenant_id,
                    "vimid": vim_id}

        controller_meta["get"] = _get

    return path, type(controller_name, (rest.RestController,), controller_meta)


def insert_dynamic_controller(root_controller):
    api_defs = utils.get_definition_list()
    for d in api_defs:
        path, con_class = _build_api_controller(d)
        setattr(root_controller, path, con_class())
