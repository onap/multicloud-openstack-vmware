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
import random
import string
import sys

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.msapi import extsys
from vio.pub.vim.vimapi.glance import OperateImage
from vio.swagger import image_utils
from vio.pub.exceptions import VimDriverVioException


class GetDeleteImageView(APIView):

    def get(self, request, vimid, tenantid, imageid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
            vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        image_op = OperateImage.OperateImage(vim_info)

        try:
            image = image_op.get_vim_image(imageid)
            vim_rsp = image_utils.vim_formatter(vim_info, tenantid)
            rsp = image_utils.image_formatter(image)
            rsp.update(vim_rsp)
            return Response(data=rsp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, vimid, tenantid, imageid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
            vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        image_op = OperateImage.OperateImage(vim_info)

        try:
            image_op.delete_vim_image(imageid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateListImagesView(APIView):

    def get(self, request, vimid, tenantid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
            vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        query_data = dict(request.query_params)
        image_instance = OperateImage.OperateImage(vim_info)

        try:
            images = image_instance.get_vim_images(**query_data)
            rsp = {}
            rsp['images'] = []
            vim_rsp = image_utils.vim_formatter(vim_info, tenantid)
            for image in images:
                rsp['images'].append(image_utils.image_formatter(image))
            rsp.update(vim_rsp)
            return Response(data=rsp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, vimid, tenantid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
            vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        try:
            req_body = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        vim_rsp = image_utils.vim_formatter(vim_info, tenantid)
        image_instance = OperateImage.OperateImage(vim_info)

        try:
            images = image_instance.get_vim_images()
            for image in images:
                if image.name == req_body.get('name'):
                    image_info = image_instance.get_vim_image(image.id)
                    rsp = image_utils.image_formatter(image_info)
                    rsp['returnCode'] = '0'
                    rsp.update(vim_rsp)
                    return Response(data=rsp, status=status.HTTP_200_OK)

            param = image_utils.req_body_formatter(req_body)
            image = image_instance.create_vim_image(vimid, tenantid,
                                                    imagePath=req_body.get(
                                                        'imagePath'),
                                                    **param)

            rsp = image_utils.image_formatter(image)
            rsp.update(vim_rsp)
            rsp['returnCode'] = '1'
            return Response(data=rsp, status=status.HTTP_201_CREATED)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateImageFileView(APIView):

    def post(self, request, vimid, tenantid):

        try:
            vim_info = extsys.get_vim_by_id(vimid)
            vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        image_instance = OperateImage.OperateImage(vim_info)

        image_file = request.FILES['file']

        random_name = ''.join(random.sample(
                                        string.ascii_letters
                                        + string.digits, 4))
        file_name = image_file.name[:image_file.name.rfind('.')]
        + "_" + random_name
        + image_file.name[image_file.name.find('.'):]

        file_dest = sys.path[0] + '/images/' + file_name
        with open(file_dest, 'wb+') as temp_file:
            for chunk in image_file.chunks():
                temp_file.write(chunk)
        temp_file.close()

        image_type = image_file.name[image_file.name.find('.') + 1:]

        try:
            image_instance.create_vim_image_file(vimid, tenantid,
                                                 file_name[:
                                                           file_name.rfind(
                                                            '.')],
                                                 file_dest,
                                                 image_type)

            return Response(data={'status': 'upload OK'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetImageFileView(APIView):

    def post(self, request, vimid, tenantid, imageid):
        try:
            vim_info = extsys.get_vim_by_id(vimid)
            vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)

        try:
            req_body = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        image_instance = OperateImage.OperateImage(vim_info)
        try:
            image = image_instance.find_vim_image(imageid)
        except Exception as e:
            return Response(data={'error': 'the image does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        try:
            image_data = image_instance.download_vim_image(image)

            imagePath = req_body.get('imagePath')
            if imagePath[-1:] is not '/':
                imagePath += '/'
            file_name = "%s%s.%s" % (imagePath, image.name, image.disk_format)
            image_file = open(file_name, 'w+')

            for chunk in image_data:
                image_file.write(chunk)
            image_file.close()

            return Response(data={'status': 'donwload OK'},
                            status=status.HTTP_200_OK)

        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
