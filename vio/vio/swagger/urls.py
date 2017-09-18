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

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from vio.swagger.views.hypervisor.views import HostView
from vio.swagger.views.limits.views import LimitsView
from vio.swagger.views.service.views import HostsView
from vio.swagger.views.swagger_json import SwaggerJsonView
from vio.swagger.views.tenant.views import ListTenantsView
from vio.swagger.views.image.views import CreateListImagesView
from vio.swagger.views.image.views import GetDeleteImageView
from vio.swagger.views.volume.views import CreateListVolumeView
from vio.swagger.views.volume.views import GetDeleteVolumeView
from vio.swagger.views.server.views import ListServersView, GetServerView
from vio.swagger.views.flavor.views import FlavorsView, FlavorView
from vio.swagger.views.network.views import CreateNetworkView
from vio.swagger.views.network.views import DeleteNetworkView
from vio.swagger.views.subnet.views import CreateSubnetView, DeleteSubnetView
from vio.swagger.views.port.views import CreatePortView, DeletePortView

# proxy
from vio.swagger.views.proxyplugin.identity.views import TokenView
from vio.swagger.views.proxyplugin.identity.views import IdentityServer
from vio.swagger.views.proxyplugin.nova.views import ComputeServer
from vio.swagger.views.proxyplugin.image.views import ImageServer
from vio.swagger.views.proxyplugin.neutron.views import NetWorkServer
from vio.swagger.views.proxyplugin.volumn.views import VolumeServer
from vio.swagger.views.proxyplugin.heat.views import HeatServer

# Registry
from vio.swagger.views.registry.views import Registry

# fake
from vio.swagger.views.fakeplugin.identity.views import FakeProjects
from vio.swagger.views.fakeplugin.identity.views import FakeToken
from vio.swagger.views.fakeplugin.image.views import FakeImage
from vio.swagger.views.fakeplugin.image.views import FakeImageDetail
from vio.swagger.views.fakeplugin.image.views import FakeImageSchema
from vio.swagger.views.fakeplugin.nova.views import FakeNovaServer
from vio.swagger.views.fakeplugin.nova.views import FakeNovaHypervisors
from vio.swagger.views.fakeplugin.nova.views import FakeNovaAggregate
from vio.swagger.views.fakeplugin.nova.views import FakeNovaHypervisorsUptime
from vio.swagger.views.fakeplugin.nova.views import FakeNovaServerDetail
from vio.swagger.views.fakeplugin.nova.views import FakeFlavorList
from vio.swagger.views.fakeplugin.nova.views import FakeFlavorDetail
from vio.swagger.views.fakeplugin.neutron.views import FakeNeutron
from vio.swagger.views.fakeplugin.neutron.views import FakeNeutronDetail
from vio.swagger.views.fakeplugin.neutron.views import FakeNeutronNetwork


urlpatterns = [
    # swagger
    url(r'^api/multicloud-vio/v0/swagger.json$', SwaggerJsonView.as_view()),

    # fake urls
    url(r'^api/multicloud-vio/v0/vmware_fake/neutron/networks$',
        FakeNeutronNetwork.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/neutron/networks/'
        r'(?P<netid>[0-9a-z-A-Z]+)$',
        FakeNeutronDetail.as_view()),

    # vio
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'tenants$', ListTenantsView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/images$',
        CreateListImagesView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/images/(?P<imageid>[0-9a-zA-Z_-]+)$',
        GetDeleteImageView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/volumes$',
        CreateListVolumeView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/volumes/(?P<volumeid>[0-9a-zA-Z_-]+)$',
        GetDeleteVolumeView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/servers$', ListServersView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/servers/(?P<serverid>[0-9a-zA-Z_-]+)$',
        GetServerView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/flavors$',
        FlavorsView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/flavors/(?P<flavorid>[0-9a-zA-Z_-]+)$',
        FlavorView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/limits$',
        LimitsView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/hosts$',
        HostsView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z]+)/hosts/(?P<hostname>[0-9a-zA-Z_-]+)$',
        HostView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)\
        /(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks$',
        CreateNetworkView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)\
        /(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks/'
        r'(?P<networkid>[0-9a-zA-Z\-\_]+)$',
        DeleteNetworkView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)\
        /(?P<tenantid>[0-9a-zA-Z\-\_]+)/subnets$',
        CreateSubnetView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)\
        /(?P<tenantid>[0-9a-zA-Z\-\_]+)/subnets/'
        r'(?P<subnetid>[0-9a-zA-Z\-\_]+)$',
        DeleteSubnetView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)\
        /(?P<tenantid>[0-9a-zA-Z\-\_]+)/ports$',
        CreatePortView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)\
        /(?P<tenantid>[0-9a-zA-Z\-\_]+)/ports/'
        r'(?P<portid>[0-9a-zA-Z\-\_]+)$',
        DeletePortView.as_view()),

    # fake urls
    url(r'^api/multicloud-vio/v0/vmware_fake/identity/v3',
        FakeToken.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/identity/projects$',
        FakeProjects.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/identity/projects/'
        r'(?P<projectid>[0-9a-z-A-Z]+)$',
        FakeProjects.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/os-hypervisors/detail$',
        FakeNovaHypervisors.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/os-hypervisors/'
        r'(?P<hyperid>[0-9a-z-A-Z]+)$',
        FakeNovaHypervisors.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/os-hypervisors/'
        r'(?P<hyperid>[0-9a-z-A-Z]+)/uptime$',
        FakeNovaHypervisorsUptime.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/os-aggregates$',
        FakeNovaAggregate.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers$',
        FakeNovaServer.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers/detail$',
        FakeNovaServerDetail.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers/'
        r'(?P<serverid>[0-9a-z-A-Z]+)$',
        FakeNovaServer.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers/'
        r'(?P<serverid>[0-9a-z-A-Z]+)/action$',
        FakeNovaServer.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/flavors$',
        FakeFlavorList.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/flavors/'
        r'(?P<flavorid>[0-9a-z-A-Z]+)$',
        FakeFlavorDetail.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/glance/v2/schemas/image$',
        FakeImageSchema.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/glance/v2/images/'
        r'(?P<imageid>[0-9a-z-A-Z\-\_]+)$',
        FakeImageDetail.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/glance/v2/images',
        FakeImage.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/glance/version',
        FakeImage.as_view()),
    url(r'^api/multicloud-vio/v0/vmware_fake/neutron$',
        FakeNeutron.as_view()),

    # Registry
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/registry$',
        .as_view()),
    # url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)$',
    #     Registry.as_view()),

    #   proxy
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/identity/v3',
        TokenView.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/identity$',
        IdentityServer.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /identity/(?P<other>(.*))$',
        IdentityServer.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /glance/(?P<other>(.*))$',
        ImageServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /cinder/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        VolumeServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /cinderv2/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        VolumeServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /cinderv3/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        VolumeServer.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/neutron$',
        NetWorkServer.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /neutron/(?P<other>(.*))$',
        NetWorkServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /heat/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        HeatServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)\
        /nova/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        ComputeServer.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
