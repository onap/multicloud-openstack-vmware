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

from keystoneauth1.identity import v2 as keystone_v2
from keystoneauth1.identity import v3 as keystone_v3
from keystoneauth1 import session
import pecan
from pecan import rest

from vio.api_v2.api_definition import utils
from vio.pub import exceptions
from vio.pub.msapi import extsys


def _get_vim_auth_session(vim_id, tenant_id):
    """ Get the auth session to backend VIM """

    try:
        vim = extsys.get_vim_by_id(vim_id)
    except exceptions.VimDriverVioException as e:
        return pecan.abort(500, str(e))

    params = {
        "auth_url": vim["url"],
        "username": vim["userName"],
        "password": vim["password"],
    }

    # tenantid takes precedence over tenantname
    if tenant_id:
        params["tenant_id"] = tenant_id
    else:
        # input tenant name takes precedence over the default one
        # from AAI data store
        params["tenant_name"] = (tenant_name if tenant_name else vim['tenant'])

    if '/v2' in params["auth_url"]:
        auth = keystone_v2.Password(**params)
    else:
        params["user_domain_name"] = vim["domain"]
        params["project_domain_name"] = vim["domain"]

        if 'tenant_id' in params:
            params["project_id"] = params.pop("tenant_id")
        if 'tenant_name' in params:
            params["project_name"] = params.pop("tenant_name")
        if '/v3' not in params["auth_url"]:
            params["auth_url"] = params["auth_url"] + "/v3",
        auth = keystone_v3.Password(**params)

    return session.Session(auth=auth)


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
    delimiter = path_meta["vim_path"].find("/", 1)
    service_type = path_meta["vim_path"][1:delimiter]
    resource_url = path_meta["vim_path"][delimiter:]

    # Assume that only one resource
    name, resource_meta = api_meta['definitions'].items()[0]
    resource_properties = resource_meta['properties']

    controller_meta = {}
    if "get" in path_meta:
        # Add get method to controller.
        @pecan.expose("json")
        def _get(self, vim_id, tenant_id, resource_id):
            """ General GET """

            session = _get_vim_auth_session(vim_id, tenant_id)
            service = {'service_type': service_type,
                       'interface': 'public'}
            full_url = resource_url + "/%s" % resource_id
            resp = session.get(full_url, endpoint_filter=service)
            mc_res = _convert_vim_res_to_mc_res(resp.json(),
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
