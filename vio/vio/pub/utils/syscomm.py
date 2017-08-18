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

import inspect
import json
from collections import defaultdict

def fun_name():
    return inspect.stack()[1][3]


def jsonResponse(data,encoding='utf-8'):

    content_type = "application/json"
    try:
        res = json.loads(data,encoding=encoding)
    except  Exception as e:
        res = data
        content_type = "text/plain"
    return (res,content_type)


class Catalogs(object):

    def __init__(self):
        self.ct=defaultdict(dict)


    def storeEndpoint(self,vimid,endpoints):
        self.ct.setdefault(vimid,endpoints)

    def getEndpointBy(self,vimid,serverType,interface='admin'):

        vim = self.ct.get(vimid)
        return vim.get(serverType).get(interface,"") if vim else ""



catalog = Catalogs()
