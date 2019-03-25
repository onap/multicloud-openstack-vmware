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


# from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.heat import OperateStack
from vio.pub.vim.vimapi.nova import OperateServers

import logging

logger = logging.getLogger(__name__)


def heat_bridge(vim_info, stack_id):
    ret = {
        "servers": []
    }
    stack_op = OperateStack.OperateStack(vim_info)
    server_op = OperateServers.OperateServers()
    data = {'vimid': vim_info['vimId'],
            'vimName': vim_info['name'],
            'username': vim_info['userName'],
            'password': vim_info['password'],
            'url': vim_info['url']}
    resources = stack_op.get_stack_resources(stack_id)
    for res in resources:
        if res.resource_type != "OS::Nova::Server":
            continue
        if not res.status.endswith("COMPLETE"):
            continue
        instance = server_op.get_server(data, None, res.physical_resource_id)
        if instance is None:
            logger.info("can not find server %s" % res.physical_resource_id)
            continue
        for link in instance.links:
            if link['rel'] == "self":
                slink = link['rel']
                break
        ret['servers'].append({
            "name": instance.name,
            "id": instance.id,
            "status": instance.status,
            "link": slink,
        })
    return ret

# if __name__ == "__main__":
#     import ipdb; ipdb.set_trace()
#     vim_info = extsys.get_vim_by_id("vmware_nova2")
#     datas = heat_bridge(vim_info, "test")
