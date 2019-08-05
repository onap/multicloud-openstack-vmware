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

import inspect
import json
from collections import defaultdict
from django.core.cache import cache
from vio.settings import CACHE_TIMEOUT
from rest_framework import status

keystoneV2Json = \
    {
        "auth": {
            "tenantName": "",
            "passwordCredentials": {
                "username": "",
                "password": ""
            }
        }
    }


SUCCESS_STATE = [status.HTTP_200_OK, status.HTTP_201_CREATED,
                 status.HTTP_202_ACCEPTED]


def fun_name():
    return inspect.stack()[1][3]


def jsonResponse(data, encoding='utf-8'):

    content_type = "application/json"
    try:
        res = json.loads(data, encoding=encoding)
    except Exception:
        res = data
        content_type = "text/plain"
    return (res, content_type)


class Catalogs(object):

    def __init__(self):
        self.ct = defaultdict(dict)

    def storeEndpoint(self, vimid, endpoints):
        cache.set(vimid, endpoints, CACHE_TIMEOUT)

    def getEndpointBy(self, vimid, serverType, interface='public'):

        if vimid in cache:
            vim = cache.get(vimid)
            return vim.get(serverType).get(interface, "")
        return None


def verifyKeystoneV2(param):

    return _walk_json(param, keystoneV2Json)


# comapare two json by key
# def _walk_json(data, data2):
#     if isinstance(data, dict) and isinstance(data2, dict):
#         if set(list(data.keys())) != set(list(data2.keys())):
#             return False
#         else:
#             v1 = list(data.values())
#             v2 = list(data2.values())
#             v1 = sorted(v1)
#             v2 = sorted(v2)
#             if len(v1) != len(v2):
#                 return False
#             for (i, j) in zip(v1, v2):
#                 # continue compare key
#                 if isinstance(i, dict) and isinstance(j, dict):
#                     if not _walk_json(i, j):
#                         return False
#                 # ignore value
#                 else:
#                     continue

#             return True

#     return False
def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def _walk_json(data, data2):
    return ordered(data) == ordered(data2)


def keystoneVersion(url, version="v3"):

    tmp = url.split("/")
    v = tmp[-1]
    if v not in ["v2.0", "v3"]:
        url += "/" + version
    else:
        tmp[-1] = version
        url = "/".join(tmp)

    return url


catalog = Catalogs()
