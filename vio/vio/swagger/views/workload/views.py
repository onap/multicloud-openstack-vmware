# Copyright (c) 2018 VMware, Inc.
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

from vio import heatbridge
from vio.pub.msapi import extsys
from vio.pub.utils.restcall import AAIClient
from vio.pub.vim.vimapi.heat import OperateStack
from vio.pub.exceptions import VimDriverVioException

logger = logging.getLogger(__name__)


def handle_directives(body):
    params = {}
    try:
        stack_params = body['template_data']['parameters']
        stack_params_keys = list(stack_params.keys())
        for oofd in body["oof_directives"]:
            if oofd["type"] == "vnfc":
                for dd in oofd["directives"]:
                    if dd["type"] == "flavor_directives":
                        for attr in dd["attributes"]:
                            params[attr[
                                "attribute_name"]] = attr["attribute_value"]
        for k, v in params.items():
            if k in stack_params_keys:
                stack_params[k] = v
    except KeyError as ex:
        logger.debug("Error handle directives: %s" % str(ex))
    return body


class CreateStackViewV1(APIView):

    def post(self, request, cloud_owner, cloud_region):
        try:
            vim_info = extsys.get_vim_by_id(cloud_owner + "_" + cloud_region)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)
        try:
            body = json.loads(request.body)
            logger.debug("infra_workload post body: %s" % body)
            template_type = body['template_type']
            if template_type.lower() != "heat":
                return Response(
                    data={
                        "error": "invalid template type %s" % template_type
                        },
                    status=status.HTTP_400_BAD_REQUEST)
            body = handle_directives(body)
            stack_body = body['template_data']
        except Exception:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            logger.debug("create stack input: %s" % stack_body)
            stack_op = OperateStack.OperateStack(vim_info)
            stack = stack_op.create_vim_stack(**stack_body)
            rsp = {
                "template_type": "heat",
                "workload_id": stack.id,
                "workload_status": stack.status,
                "workload_status_reason": stack.status_reason,
            }
            return Response(data=rsp, status=status.HTTP_201_CREATED)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetDelStackViewV1(APIView):
    def get(self, request, cloud_owner, cloud_region, workload_id):
        # import ipdb; ipdb.set_trace()
        try:
            vim_info = extsys.get_vim_by_id(cloud_owner + "_" + cloud_region)
            # vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)
        try:
            stack_op = OperateStack.OperateStack(vim_info)
            stack = stack_op.get_vim_stack(workload_id)
            # import ipdb; ipdb.set_trace()
            rsp = {
                "template_type": "heat",
                "workload_id": stack.id,
                "workload_status": stack.status,
                "workload_status_reason": stack.status_reason,
            }
            return Response(data=rsp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, cloud_owner, cloud_region, workload_id):
        # import ipdb; ipdb.set_trace()
        try:
            vim_info = extsys.get_vim_by_id(cloud_owner + "_" + cloud_region)
            # vim_info['tenant'] = tenantid
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)
        try:
            body = json.loads(request.body)
            vf_module_id = body.get("vf-module-id")
            generic_vnf_id = body.get("generic-vnf-id")
            contents = heatbridge.heat_bridge(vim_info, workload_id)
            contents['vf-module-id'] = vf_module_id
            contents['generic-vnf-id'] = generic_vnf_id
            aai_adapter = AAIClient(cloud_owner, cloud_region)
            aai_adapter.add_vservers(contents)
            rsp = {
                "template_type": "heat",
                "workload_id": workload_id,
                "workload_status": "AAI_IN_PROGRESS",
                "workload_status_reason": "Updating AAI relationship",
            }
            return Response(data=rsp, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, cloud_owner, cloud_region, workload_id):
        try:
            vim_info = extsys.get_vim_by_id(cloud_owner + "_" + cloud_region)
        except VimDriverVioException as e:
            return Response(data={'error': str(e)}, status=e.status_code)
        try:
            stack_op = OperateStack.OperateStack(vim_info)
            stack_op.delete_vim_stack(workload_id)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
