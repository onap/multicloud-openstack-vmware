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

import unittest
import mock
from rest_framework import status
from vio.swagger.views.registry.views import Registry


from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.keystone.OperateTenant import OperateTenant
from vio.pub.vim.vimapi.glance.OperateImage import OperateImage

VIM_INFO = {'vimId': 1, 'name': 'name1', 'userName': 'user1',
            'password': '1234', 'url': 'abc', 'tenant': 't1'}


class RegistryViewTest(unittest.TestCase):

    def setUp(self):
        self.reg = Registry()

    def tearDown(self):
        pass

    @mock.patch.object(OperateTenant, 'get_projects')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_reg_delete_view(self, mock_vim_info, mock_projects):
        mock_vim_info.return_value = VIM_INFO

        class Project:
            def __init__(self, id, name):
                self.id = id
                self.name = name
        p1 = Project(1, "p1")
        p2 = Project(2, "p2")
        projects = [p1, p2]
        mock_projects.return_value = projects

        class Request:
            def __init__(self, query_params):
                self.query_params = query_params
        req = Request({'k': 'v'})
        self.assertEqual(
            status.HTTP_200_OK,
            self.reg.delete(req, "vimid").status_code)

    @mock.patch.object(OperateTenant, 'get_projects')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_reg_get_tenants_view(self, mock_vim_info, mock_projects):
        mock_vim_info.return_value = VIM_INFO

        class Project:
            def __init__(self, id, name):
                self.id = id
                self.name = name

            def to_dict(self):
                return {"name": self.name, "id": self.id}
        p1 = Project(1, "p1")
        p2 = Project(2, "p2")
        projects = [p1, p2]
        mock_projects.return_value = projects

        self.assertEqual(
            {'tenants': [{'id': 1, 'name': 'p1'}, {'id': 2, 'name': 'p2'}]},
            self.reg._get_tenants("vimid"))

    @mock.patch.object(OperateTenant, 'get_projects')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_reg_get_tenants_view_fail(self, mock_vim_info, mock_projects):
        mock_vim_info.return_value = VIM_INFO

        mock_projects.side_effect = TypeError("wrong type")

        self.assertEqual(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            self.reg._get_tenants("vimid").status_code)

    @mock.patch.object(OperateImage, 'get_vim_images')
    @mock.patch.object(extsys, 'get_vim_by_id')
    def test_reg_get_images_view(self, mock_vim_info, mock_images):
        mock_vim_info.return_value = VIM_INFO

        class Image:
            def __init__(self, id, name):
                self.id = id
                self.name = name

            def to_dict(self):
                return {"name": self.name, "id": self.id}
        i1 = Image(1, "i1")
        i2 = Image(2, "i2")
        images = [i1, i2]
        mock_images.return_value = images

        class Auth:
            def __init__(self, id):
                self.id = id

            def get(self, username):
                self.username = username
        a = Auth(1)
        self.assertEqual(
            {'images': [{'id': 1, 'name': 'i1'}, {'id': 2, 'name': 'i2'}]},
            self.reg._get_images(a))
