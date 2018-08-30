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
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from vio.pub.utils import syscomm
from vio.pub.vim.vimapi.network import OperateNetwork

logger = logging.getLogger(__name__)


class CreateNetworkView(APIView):
    def post(self, request, vimid, tenantid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        net = OperateNetwork.OperateNetwork()
        try:
            body = json.loads(request.body)
        except Exception as e:
            return Response(data={'error': 'Fail to decode request body.'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            req_paras = ["name", "shared"]
            for para in req_paras:
                if para not in body:
                    raise Exception('Required parameter %s is '
                                    'missing in net creation.' % para)
            network_name = body.get('name')
            network_id = body.get('id', None)
            target = network_id or network_name
            resp = net.list_network(vimid, tenantid, target)
            if resp:
                resp['returnCode'] = 0
                return Response(data=resp, status=status.HTTP_200_OK)
            else:
                resp = net.create_network(vimid, tenantid, body)
                resp['returnCode'] = 1
                return Response(data=resp, status=status.HTTP_201_CREATED)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, vimid, tenantid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        query = dict(request.query_params)
        net = OperateNetwork.OperateNetwork()
        try:
            resp = net.list_networks(vimid, tenantid, **query)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateNetworkViewV1(CreateNetworkView):
    def post(self, request, cloud_owner, cloud_region, tenantid):
        return super(CreateNetworkViewV1, self).post(
            request, cloud_owner + "_" + cloud_region, tenantid)

    def get(self, request, cloud_owner, cloud_region, tenantid):
        return super(CreateNetworkViewV1, self).get(
            request, cloud_owner + "_" + cloud_region, tenantid)


class DeleteNetworkView(APIView):

    def get(self, request, vimid, tenantid, networkid):
        if vimid == "vmware_fake":
            return Response(data={
                "vimid": vimid,
                "vimName": vimid,
                "tenantId": tenantid,
                "status": "ACTIVE",
                "segmentationId": None,
                "name": "oam_onap_AQYG",
                "physicalNetwork": None,
                "shared": False,
                "routerExternal": False,
                "networkType": None,
                "vlanTransparent": False,
                "id": "0085970f-a214-4da2-a449-75acfb813fec"
            }, status=status.HTTP_200_OK)

        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        net = OperateNetwork.OperateNetwork()
        try:
            resp = net.list_network(vimid, tenantid, networkid)
            return Response(data=resp, status=status.HTTP_200_OK)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, vimid, tenantid, networkid):
        logger.info("Enter %s, method is %s, vim_id is %s",
                    syscomm.fun_name(), request.method, vimid)
        net = OperateNetwork.OperateNetwork()
        try:
            resp = net.delete_network(vimid, tenantid, networkid)
            return Response(data=resp, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            if hasattr(e, "http_status"):
                return Response(data={'error': str(e)}, status=e.http_status)
            else:
                return Response(data={'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteNetworkViewV1(DeleteNetworkView):
    def get(self, request, cloud_owner, cloud_region, tenantid, networkid):
        return super(DeleteNetworkViewV1, self).get(
            request, cloud_owner + "_" + cloud_region, tenantid, networkid)

    def delete(self, request, cloud_owner, cloud_region, tenantid, networkid):
        return super(DeleteNetworkViewV1, self).delete(
            request, cloud_owner + "_" + cloud_region, tenantid, networkid)
