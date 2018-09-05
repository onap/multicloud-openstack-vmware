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

import logging

# from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.baseclient import baseclient

logger = logging.getLogger(__name__)


def sdk_param_formatter(data):
    param = {}
    param['username'] = data.get('userName')
    param['password'] = data.get('password')
    param['auth_url'] = data.get('url')
    param['project_id'] = data.get('tenant')
    param['user_domain_name'] = 'default'
    param['project_domain_name'] = 'default'
    return param


class OperateStack(baseclient):

    def __init__(self, params):
        super(OperateStack, self).__init__()
        self.param = sdk_param_formatter(params)

    def get_vim_stacks(self, **query):

        stacks = self.heat(self.param).stack_list(**query)
        return stacks

    def create_vim_stack(self, **body):

        stack = self.heat(self.param).stack_create(**body)
        return stack

    def get_vim_stack(self, stack_id):

        stack = self.heat(self.param).stack_find(stack_id)
        return stack

    def delete_vim_stack(self, stack_id):

        stack = self.heat(self.param).stack_delete(stack_id)
        return stack
