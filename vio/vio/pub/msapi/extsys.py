# Copyright (c) 2017 VMware, Inc.
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
from vio.pub.exceptions import VimDriverVioException
from vio.pub.utils.restcall import AAIClient

logger = logging.getLogger(__name__)


# def get_vims():
#     ret = req_by_msb("/openoapi/extsys/v1/vims", "GET")
#     if ret[0] != 0:
#         logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
#         raise VimDriverVioException("Failed to query VIMs from extsys.")
#     return json.JSONDecoder().decode(ret[1])


# def get_vim_by_id(vim_id):
#     ret = req_by_msb("/openoapi/extsys/v1/vims/%s" % vim_id, "GET")
#     if ret[0] != 0:
#         logger.error("Status code is %s, detail is %s.", ret[2], ret[1])
#         raise VimDriverVioException("Failed to query VIM with id (%s) from extsys." % vim_id,
#                                     status.HTTP_404_NOT_FOUND)
#     return json.JSONDecoder().decode(ret[1])


def split_vim_to_owner_region(vim_id):
    split_vim = vim_id.split('_')
    cloud_owner = split_vim[0]
    cloud_region = "".join(split_vim[1:])
    return cloud_owner, cloud_region


def get_vim_by_id(vim_id):
    cloud_owner, cloud_region = split_vim_to_owner_region(vim_id)
    client = AAIClient(cloud_owner, cloud_region)
    ret = client.get_vim(get_all=True)
    ret['type'] = ret['cloud-type']
    ret['version'] = ret['cloud-region-version']
    ret['vimId'] = vim_id
    # fix here after aai schema is ready
    # ret['username'] = ret['auth-info-items']['username']
    # ret['password'] = ret['auth-info-items']['password']
    # ret['tenant'] = ret['auth-info-items']['tenant']
    # ret['url'] = ret['auth-info-items']['auth-url']
    return ret
