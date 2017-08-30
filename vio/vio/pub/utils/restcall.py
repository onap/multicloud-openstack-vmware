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

import sys
import traceback
import logging
import urllib2
import uuid
import httplib2
import json

from vio.pub.config.config import AAI_SCHEMA_VERSION
from vio.pub.config.config import AAI_SERVICE_URL
from vio.pub.config.config import AAI_USERNAME
from vio.pub.config.config import AAI_PASSWORD
from vio.pub.config.config import MSB_SERVICE_IP, MSB_SERVICE_PORT

from vio.pub.exceptions import VimDriverVioException

rest_no_auth, rest_oneway_auth, rest_bothway_auth = 0, 1, 2
HTTP_200_OK, HTTP_201_CREATED = '200', '201'
HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED = '204', '202'
status_ok_list = [HTTP_200_OK, HTTP_201_CREATED,
                  HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED]
HTTP_404_NOTFOUND, HTTP_403_FORBIDDEN = '404', '403'
HTTP_401_UNAUTHORIZED, HTTP_400_BADREQUEST = '401', '400'

logger = logging.getLogger(__name__)


def call_req(base_url, user, passwd, auth_type, resource, method, content='',
             headers=None):
    callid = str(uuid.uuid1())
#    logger.debug("[%s]call_req('%s','%s','%s',%s,'%s','%s','%s')" % (
#        callid, base_url, user, passwd, auth_type, resource, method, content))
    ret = None
    resp_status = ''
    resp = ""
    full_url = ""

    try:
        full_url = combine_url(base_url, resource)
        if headers is None:
            headers = {}
            headers['content-type'] = 'application/json'

        if user:
            headers['Authorization'] = 'Basic ' + \
                ('%s:%s' % (user, passwd)).encode("base64")
        ca_certs = None
        for retry_times in range(3):
            http = httplib2.Http(
                ca_certs=ca_certs,
                disable_ssl_certificate_validation=(
                    auth_type == rest_no_auth))
            http.follow_all_redirects = True
            try:
                logger.debug("request=%s" % full_url)
                resp, resp_content = http.request(
                    full_url, method=method.upper(), body=content,
                    headers=headers)
                resp_status = resp['status']
                resp_body = resp_content.decode('UTF-8')

                if resp_status in status_ok_list:
                    ret = [0, resp_body, resp_status, resp]
                else:
                    ret = [1, resp_body, resp_status, resp]
                break
            except Exception as ex:
                if 'httplib.ResponseNotReady' in str(sys.exc_info()):
                    logger.error(traceback.format_exc())
                    ret = [1, "Unable to connect to %s" % full_url,
                           resp_status, resp]
                    continue
                raise ex
    except urllib2.URLError as err:
        ret = [2, str(err), resp_status, resp]
    except Exception as ex:
        logger.error(traceback.format_exc())
        logger.error("[%s]ret=%s" % (callid, str(sys.exc_info())))
        res_info = str(sys.exc_info())
        if 'httplib.ResponseNotReady' in res_info:
            res_info = ("The URL[%s] request failed or is not responding." %
                        full_url)
        ret = [3, res_info, resp_status, resp]
    except:
        logger.error(traceback.format_exc())
        ret = [4, str(sys.exc_info()), resp_status, resp]

#    logger.debug("[%s]ret=%s" % (callid, str(ret)))
    return ret


def req_by_msb(resource, method, content=''):
    base_url = "http://%s:%s/" % (MSB_SERVICE_IP, MSB_SERVICE_PORT)
    return call_req(base_url, "", "", rest_no_auth, resource, method, content)


def combine_url(base_url, resource):
    full_url = None
    if base_url.endswith('/') and resource.startswith('/'):
        full_url = base_url[:-1] + resource
    elif base_url.endswith('/') and not resource.startswith('/'):
        full_url = base_url + resource
    elif not base_url.endswith('/') and resource.startswith('/'):
        full_url = base_url + resource
    else:
        full_url = base_url + '/' + resource
    return full_url


def get_res_from_aai(resource, content=''):
    headers = {
        'X-FromAppId': 'MultiCloud',
        'X-TransactionId': '9001',
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    base_url = "%s/%s" % (AAI_SERVICE_URL, AAI_SCHEMA_VERSION)
    return call_req(base_url, AAI_USERNAME, AAI_PASSWORD, rest_no_auth,
                    resource, "GET", content, headers)


class AAIClient(object):
    def __init__(self, cloud_owner, cloud_region):
        self.base_url = "%s/%s" % (AAI_SERVICE_URL, AAI_SCHEMA_VERSION)
        self.username = AAI_USERNAME
        self.password = AAI_PASSWORD
        self.default_headers = {
            'X-FromAppId': 'multicloud-openstack-vmware',
            'X-TransactionId': '9004',
            'content-type': 'application/json',
            'accept': 'application/json'
        }
        self.cloud_owner = cloud_owner
        self.cloud_region = cloud_region

    def get_vim(self, get_all=False):
        resource = ("/cloud-infrastructure/cloud-regions/cloud-region"
                    "/%s/%s" % (self.cloud_owner, self.cloud_region))
        if get_all:
            resource = "%s?depth=all" % resource
        resp = call_req(self.base_url, self.username, self.password,
                        rest_no_auth, resource, "GET",
                        headers=self.default_headers)
        if resp[0] != 0:
            raise VimDriverVioException(
                status_code=404,
                content="Failed to query VIM with id (%s_%s) from extsys." % (
                    self.cloud_owner, self.cloud_region))
        return json.loads(resp[1])

    def delete_vim(self):
        resource = ("/cloud-infrastructure/cloud-regions/cloud-region"
                    "/%s/%s" % (self.cloud_owner, self.cloud_region))
        resp = call_req(self.base_url, self.username, self.password,
                        rest_no_auth, resource, "DELETE",
                        headers=self.default_headers)
        if resp[0] != 0:
            raise VimDriverVioException(
                status_code=400,
                content="Failed to delete cloud %s_%s: %s." % (
                    self.cloud_owner, self.cloud_region, resp[1]))
        return json.loads(resp[1])

    def update_vim(self, content):
        # update identity url
        self.update_identity_url()
        # update tenants
        self.add_tenants(content)
        # update flavors
        self.add_images(content)
        # update images
        self.add_flavors(content)
        # update pservers
        self.add_pservers(content)

    def update_identity_url(self):
        vim = self.get_vim()
        vim['identity-url'] = ("http://%s/api/multicloud/v0/%s_%s/identity/"
                               "v3" % (MSB_SERVICE_IP, self.cloud_owner,
                                       self.cloud_region))
        resource = ("/cloud-infrastructure/cloud-regions/cloud-region"
                    "/%s/%s" % (self.cloud_owner, self.cloud_region))
        call_req(self.base_url, self.username, self.password,
                 rest_no_auth, resource, "PUT",
                 content=json.dumps(vim),
                 headers=self.default_headers)

    def add_tenants(self, content):
        for tenant in content['tenants']:
            resource = ("/cloud-infrastructure/cloud-regions/cloud-region/"
                        "%s/%s/tenants/tenant/%s" % (
                            self.cloud_owner, self.cloud_region, tenant['id']))
            body = {'tenant-name': tenant['name']}
            call_req(self.base_url, self.username, self.password,
                     rest_no_auth, resource, "PUT",
                     content=json.dumps(body),
                     headers=self.default_headers)

    def add_flavors(self, content):
        for flavor in content['flavors']:
            resource = ("/cloud-infrastructure/cloud-regions/cloud-region/"
                        "%s/%s/flavors/flavor/%s" % (
                            self.cloud_owner, self.cloud_region, flavor['id']))
            body = {
                'flavor-name': flavor['name'],
                'flavor-vcpus': flavor['vcpus'],
                'flavor-ram': flavor['ram'],
                'flavor-disk': flavor['disk'],
                'flavor-ephemeral': flavor['ephemeral'],
                'flavor-swap': flavor['swap'],
                'flavor-is-public': flavor['is_public'],
                'flavor-selflink': flavor['links'][0]['href'],
                'flavor-disabled': flavor['is_disabled']
            }
            call_req(self.base_url, self.username, self.password,
                     rest_no_auth, resource, "PUT",
                     content=json.dumps(body),
                     headers=self.default_headers)

    def add_images(self, content):
        for image in content['images']:
            resource = ("/cloud-infrastructure/cloud-regions/cloud-region/"
                        "%s/%s/images/image/%s" % (
                            self.cloud_owner, self.cloud_region, image['id']))
            body = {
                'image-name': image['name'],
                # 'image-architecture': image[''],
                'image-os-distro': image['name'].split("-")[0],
                'image-os-version': image['name'].split("-")[1],
                # 'application': image[''],
                # 'application-vendor': image[''],
                # 'application-version': image[''],
                # TODO replace this with image proxy endpoint
                'image-selflink': "",
            }
            call_req(self.base_url, self.username, self.password,
                     rest_no_auth, resource, "PUT",
                     content=json.dumps(body),
                     headers=self.default_headers)

    def add_pservers(self, content):
        for hypervisor in content['hypervisors']:
            resource = ("/cloud-infrastructure/pservers/pserver/%s" % (
                hypervisor['name']))
            body = {
                # 'ptnii-equip-name'
                'number-of-cpus': hypervisor['vcpus'],
                'disk-in-gigabytes': hypervisor['local_disk_size'],
                'ram-in-megabytes': hypervisor['memory_size'],
                # 'equip-type'
                # 'equip-vendor'
                # 'equip-model'
                # 'fqdn'
                # 'pserver-selflink'
                'ipv4-oam-address': hypervisor['host_ip'],
                # 'serial-number'
                # 'ipaddress-v4-loopback-0'
                # 'ipaddress-v6-loopback-0'
                # 'ipaddress-v4-aim'
                # 'ipaddress-v6-aim'
                # 'ipaddress-v6-oam'
                # 'inv-status'
                'pserver-id': hypervisor['id'],
                # 'internet-topology'
            }
            call_req(self.base_url, self.username, self.password,
                     rest_no_auth, resource, "PUT",
                     content=json.dumps(body),
                     headers=self.default_headers)
            # update relationship
            resource = ("/cloud-infrastructure/pservers/pserver/%s/"
                        "relationship-list/relationship" %
                        hypervisor['name'])
            related_link = ("%s/cloud-infrastructure/cloud-regions/"
                            "cloud-region/%s/%s" % (
                                self.base_url, self.cloud_owner,
                                self.cloud_region))
            body = {
                'related-to': 'cloud-region',
                'related-link': related_link,
                'relationship-data': [
                    {
                        'relationship-key': 'cloud-region.cloud-owner',
                        'relationship-value': self.cloud_owner
                    },
                    {
                        'relationship-key': 'cloud-region.cloud-region-id',
                        'relationship-value': self.cloud_region
                    }
                ]
            }
            call_req(self.base_url, self.username, self.password,
                     rest_no_auth, resource, "PUT",
                     content=json.dumps(body),
                     headers=self.default_headers)
