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

from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from vio.swagger.views.hypervisor.views import HostView
from vio.swagger.views.limits.views import LimitsView
from vio.swagger.views.service.views import HostsView
from vio.swagger.views.swagger_json import SwaggerJsonView
from vio.swagger.views.tenant.views import ListTenantsView
from vio.swagger.views.image.views import CreateListImagesView
from vio.swagger.views.image.views import GetDeleteImageView
from vio.swagger.views.image.views import CreateImageFileView
from vio.swagger.views.image.views import GetImageFileView
from vio.swagger.views.volume.views import CreateListVolumeView
from vio.swagger.views.volume.views import GetDeleteVolumeView
from vio.swagger.views.server.views import ListServersView, GetServerView
from vio.swagger.views.flavor.views import FlavorsView, FlavorView
from vio.swagger.views.network.views import CreateNetworkView
from vio.swagger.views.network.views import DeleteNetworkView
from vio.swagger.views.subnet.views import CreateSubnetView, DeleteSubnetView
from vio.swagger.views.port.views import CreatePortView, DeletePortView

# V1 API
from vio.swagger.views.image.views import CreateListImagesViewV1
from vio.swagger.views.image.views import GetDeleteImageViewV1
from vio.swagger.views.image.views import CreateImageFileViewV1
from vio.swagger.views.image.views import GetImageFileViewV1
from vio.swagger.views.volume.views import CreateListVolumeViewV1
from vio.swagger.views.volume.views import GetDeleteVolumeViewV1
from vio.swagger.views.server.views import ListServersViewV1, GetServerViewV1
from vio.swagger.views.flavor.views import FlavorsViewV1, FlavorViewV1
from vio.swagger.views.limits.views import LimitsViewV1
from vio.swagger.views.hypervisor.views import HostViewV1

# proxy
from vio.swagger.views.proxyplugin.identity.views import TokenView
from vio.swagger.views.proxyplugin.identity.views import TokenV2View
from vio.swagger.views.proxyplugin.identity.views import IdentityServer
from vio.swagger.views.proxyplugin.identity.views import IdentityVersionLink
from vio.swagger.views.proxyplugin.nova.views import ComputeServer
from vio.swagger.views.proxyplugin.image.views import ImageServer
from vio.swagger.views.proxyplugin.image.views import ImageVersionLink
from vio.swagger.views.proxyplugin.neutron.views import NetWorkServer
from vio.swagger.views.proxyplugin.neutron.views import NetworkVersionLink
from vio.swagger.views.proxyplugin.volumn.views import VolumeServer
from vio.swagger.views.proxyplugin.heat.views import HeatServer
from vio.swagger.views.proxyplugin.dns.views import DesignateServer
from vio.swagger.views.proxyplugin.dns.views import DesignateVersionLink

# Registry
from vio.swagger.views.registry.views import Registry
from vio.swagger.views.registry.views import UnRegistry

# Capacity Check
from vio.swagger.views.capacity.views import CapacityCheck

# Extensions
from vio.swagger.views.extensions.views import Extensions

# fake
from vio.swagger.views.fakeplugin.identity.views import FakeProjects
from vio.swagger.views.fakeplugin.identity.views import FakeTenants
from vio.swagger.views.fakeplugin.identity.views import FakeToken
from vio.swagger.views.fakeplugin.identity.views import FakeTokenV2
from vio.swagger.views.fakeplugin.image.views import FakeImage
from vio.swagger.views.fakeplugin.image.views import FakeImageVersion
from vio.swagger.views.fakeplugin.image.views import FakeImageDetail
from vio.swagger.views.fakeplugin.image.views import FakeImageSchema
from vio.swagger.views.fakeplugin.image.views import FakeImageDownload
from vio.swagger.views.fakeplugin.image.views import FakeImageUpload
from vio.swagger.views.fakeplugin.nova.views import FakeCapacity
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
from vio.swagger.views.fakeplugin.heat.views import FakeHeatResources
from vio.swagger.views.fakeplugin.heat.views import FakeHeatService
from vio.swagger.views.fakeplugin.heat.views import FakeHeatServicePreview


urlpatterns = [
    # swagger
    url(r'^api/multicloud-vio/v0/swagger.json$', SwaggerJsonView.as_view()),

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
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/images/file$',
        CreateImageFileView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z_-]+)/'
        r'(?P<tenantid>[0-9a-zA-Z_-]+)/images/file/'
        r'(?P<imageid>[0-9a-zA-Z_-]+)$',
        GetImageFileView.as_view()),
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
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks$',
        CreateNetworkView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/networks/'
        r'(?P<networkid>[0-9a-zA-Z\-\_]+)$',
        DeleteNetworkView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/subnets$',
        CreateSubnetView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/subnets/'
        r'(?P<subnetid>[0-9a-zA-Z\-\_]+)$',
        DeleteSubnetView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/ports$',
        CreatePortView.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-zA-Z\-\_]+)/'
        r'(?P<tenantid>[0-9a-zA-Z\-\_]+)/ports/'
        r'(?P<portid>[0-9a-zA-Z\-\_]+)$',
        DeletePortView.as_view()),

    # V1 urls
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z_-]+)/'
        r'images$',
        CreateListImagesViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z_-]+)/'
        r'images/(?P<imageid>[0-9a-zA-Z_-]+)$',
        GetDeleteImageViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z_-]+)/'
        r'images/file$',
        CreateImageFileViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z_-]+)/'
        r'images/file/(?P<imageid>[0-9a-zA-Z_-]+)$',
        GetImageFileViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z_-]+)/'
        r'volumes$',
        CreateListVolumeViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z_-]+)/'
        r'volumes/(?P<volumeid>[0-9a-zA-Z_-]+)$',
        GetDeleteVolumeViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z]+)/'
        r'servers$',
        ListServersViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z]+)/'
        r'servers/(?P<serverid>[0-9a-zA-Z_-]+)$',
        GetServerViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z]+)/'
        r'flavors$',
        FlavorsViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z]+)/'
        r'flavors/(?P<flavorid>[0-9a-zA-Z_-]+)$',
        FlavorViewV1.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z]+)/'
        r'limits$',
        LimitsViewV1.as_view()),
    url(r'^api/multicloud-vio/v1/(?P<cloud_owner>[0-9a-zA-Z_-]+)/'
        r'(?P<cloud_region>[0-9a-zA-Z_-]+)/(?P<tenantid>[0-9a-zA-Z]+)/'
        r'hosts/(?P<hostname>[0-9a-zA-Z_-]+)$',
        HostViewV1.as_view()),

    # fake urls
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/neutron/networks$',
        FakeNeutronNetwork.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/neutron/networks/'
        r'(?P<netid>[0-9a-z-A-Z]+)$',
        FakeNeutronDetail.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/capacity_check$',
        FakeCapacity.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/identity/v3',
        FakeToken.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/identity/v2.0',
        FakeTokenV2.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/identity/projects$',
        FakeProjects.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/identity/projects/'
        r'(?P<projectid>[0-9a-z-A-Z]+)$',
        FakeProjects.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/identity/tenants',
        FakeTenants.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/os-hypervisors/detail$',
        FakeNovaHypervisors.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/os-hypervisors/'
        r'(?P<hyperid>[0-9a-z-A-Z]+)$',
        FakeNovaHypervisors.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/os-hypervisors/'
        r'(?P<hyperid>[0-9a-z-A-Z]+)/uptime$',
        FakeNovaHypervisorsUptime.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/os-aggregates$',
        FakeNovaAggregate.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers$',
        FakeNovaServer.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers/detail$',
        FakeNovaServerDetail.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers/'
        r'(?P<serverid>[0-9a-z-A-Z]+)$',
        FakeNovaServer.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/servers/'
        r'(?P<serverid>[0-9a-z-A-Z]+)/action$',
        FakeNovaServer.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/flavors$',
        FakeFlavorList.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/nova/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)/flavors/'
        r'(?P<flavorid>[0-9a-z-A-Z]+)$',
        FakeFlavorDetail.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/glance/v2/schemas/image$',
        FakeImageSchema.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/glance/v2/images/'
        r'(?P<imageid>[0-9a-z-A-Z\-\_]+)$',
        FakeImageDetail.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/glance/v2/images',
        FakeImage.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/glance/v2/image/file/'
        r'(?P<imageid>[0-9a-z-A-Z\-\_]+)$',
        FakeImageDownload.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/glance/v2/image/file$',
        FakeImageUpload.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/glance/version',
        FakeImageVersion.as_view()),
    url(r'^api/multicloud-vio/v[01]/vmware[_/]fake/neutron$',
        FakeNeutron.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/heat/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/stacks/(?P<stack_id>[0-9a-z-A-Z\-\_]+)/resources$',
        FakeHeatResources.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/heat/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/stacks$', FakeHeatService.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/heat/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/stacks/preview$', FakeHeatServicePreview.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/heat/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/stacks/(?P<stackName>[0-9a-z-A-Z\-\_]+)',
        FakeHeatService.as_view()),
    url(r'api/multicloud-vio/v[01]/vmware[_/]fake/heat/'
        r'(?P<tenantid>[0-9a-z-A-Z\-\_]+)'
        r'/stacks/(?P<stackName>[0-9a-z-A-Z\-\_]+)'
        r'/(?P<stackID>[0-9a-z-A-Z\-\_]+)$', FakeHeatService.as_view()),

    # Registry
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/registry$',
        Registry.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)$',
        UnRegistry.as_view()),

    # CapacityCheck
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/capacity_check$',
        CapacityCheck.as_view()),

    #   proxy
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/identity/v3',
        TokenView.as_view()),
    url(r'api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/identity/v2.0$',
        TokenV2View.as_view()),
    url(r'api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)'
        r'/identity/v2.0/tokens$',
        TokenV2View.as_view()),
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/identity$',
        IdentityVersionLink.as_view()),
    # handler the rest of identity requests
    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'identity/(?P<other>(.*))$',
        IdentityServer.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/glance$',
        ImageVersionLink.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'glance/(?P<other>(.*))$',
        ImageServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'cinder/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        VolumeServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'cinderv2/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        VolumeServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'cinderv3/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        VolumeServer.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/neutron$',
        NetworkVersionLink.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'neutron/(?P<other>(.*))$',
        NetWorkServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'heat/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        HeatServer.as_view()),

    url(
        r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'nova/(?P<tenantid>[0-9a-z-A-Z\-\_]+)/(?P<other>(.*))$',
        ComputeServer.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/designate$',
        DesignateVersionLink.as_view()),

    url(r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)/'
        r'designate/(?P<other>(.*))$',
        DesignateServer.as_view()),

    # Extensions
    url(
        (r'^api/multicloud-vio/v0/(?P<vimid>[0-9a-z-A-Z\-\_]+)'
         r'/extensions$'),
        Extensions.as_view()),

]

urlpatterns = format_suffix_patterns(urlpatterns)
