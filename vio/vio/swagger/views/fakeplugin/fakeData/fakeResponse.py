
from vio.pub.config.config import MSB_SERVICE_PORT
from vio.pub.config.config import MSB_SERVICE_IP

from collections import defaultdict
from datetime import datetime
from datetime import timedelta
import copy

MSB_SERVER = MSB_SERVICE_IP + ":" + MSB_SERVICE_PORT
API_NAMESPACE = "api/multicloud-vio/v0/vmware_fake/heat"

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00" \
        "TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
        "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4" \
        "bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"

Tenantid = "c049d4ad1dee475db8c3627bef9e916a"

InitialServer = "764e369e-a874-4401-b7ce-43e4760888da"

Imageid = "70a599e0-31e7-49b7-b260-868f441e862b"


null = "null"
false = "false"
true = "true"

serverMapps = defaultdict(dict)

serverMapps[InitialServer] = \
    {
    "name": "new-server-test",
    "tenantid": Tenantid,
    "status": "BUILDING",
    'createTime': (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
    "turnStatusTime": datetime.now()
    }


def keystone_version():

    data = {
        "version": {
            "status": "stable",
            "updated": "2016-04-04T00:00:00Z",
            "media-types": [
                {
                    "base": "application/json",
                    "type": "application/vnd.openstack.identity-v3+json"
                }
            ],
            "id": "v3.6",
            "links": [
                {
                    "href": "http://" + MSB_SERVER +
                            "/api/multicloud-vio/v0/vmware_fake/identity/v3",
                    "rel": "self"
                }
            ]
        }

    }

    data['version']['update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return data


def keystone_version2():

    data = {
                "version": {
                    "status": "deprecated",
                    "updated": "2016-08-04T00:00:00Z",
                    "media-types": [
                        {
                            "base": "application/json",
                            "type": "application/"
                                    "vnd.openstack.identity-v2.0+json"
                        }
                    ],
                    "id": "v2.0",
                    "links": [
                        {
                            "href": "http://" + MSB_SERVER +
                                    "/api/multicloud-vio/"
                                    "v0/vmware_fake/identity/v2.0",
                            "rel": "self"
                        },
                        {
                            "href": "https://docs.openstack.org/",
                            "type": "text/html",
                            "rel": "describedby"
                        }
                    ]
                }
            }

    return data


def keystone_token(teanatid=None):

    data = {
        "token": {
            "value": Token,
            "methods": [
                "password"
            ],
            "roles": [
                {
                    "id": "dcce1ac133ce4db98e10070cbf56108f",
                    "name": "admin"
                }
            ],

            "expires_at": (datetime.now() +
                           timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "project": {
                "domain": {
                    "id": "c049d4ad1dee475db8c3627bef9e916a",
                    "name": "local"
                },
                "id": Tenantid,
                "name": "admin"
            },
            "catalog": [
                {
                    "endpoints": [
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/cinder/" + Tenantid,
                            "interface": "admin",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"
                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/cinder/" + Tenantid,
                            "interface": "public",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/cinder/" + Tenantid,
                            "interface": "internal",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        }
                    ],
                    "type": "volume",
                    "id": "3e4941704e9941a582b157ac7203ec1b",
                    "name": "cinder"
                },

                {
                    "endpoints": [
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/neutron",
                            "interface": "admin",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"
                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/neutron",
                            "interface": "public",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        },
                        {

                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/neutron",
                            "interface": "internal",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        }
                    ],
                    "type": "network",
                    "id": "5ef5f5a07e7848bf8f5882785a91177a",
                    "name": "neutron"
                },
                {
                    "endpoints": [
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/identity",
                            "interface": "admin",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"
                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/identity",
                            "interface": "public",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/identity",
                            "interface": "internal",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        }
                    ],
                    "type": "identity",
                    "id": "915d109fadcd40e498f3412f317169c6",
                    "name": "keystone"
                },

                {
                    "endpoints": [
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/heat/" + Tenantid,
                            "interface": "admin",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"
                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/heat/" + Tenantid,
                            "interface": "public",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/heat/" + Tenantid,
                            "interface": "internal",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        }
                    ],
                    "type": "orchestration",
                    "id": "9a6ce7f797ad48f68b46dc11dbc1258d",
                    "name": "heat"

                },
                {
                    "endpoints": [
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/nova/" + Tenantid,
                            "interface": "admin",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"
                        },

                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/nova/" + Tenantid,
                            "interface": "public",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/nova/" + Tenantid,
                            "interface": "internal",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        }
                    ],
                    "type": "compute",
                    "id": "a99dcae3c15e492db80e9e1994306b6d",
                    "name": "nova"
                },

                {
                    "endpoints": [
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/glance",
                            "interface": "admin",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"
                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/glance",
                            "interface": "public",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        },
                        {
                            "url": "http://" + MSB_SERVER +
                                   "/api/multicloud-vio/"
                                   "v0/vmware_fake/glance",
                            "interface": "internal",
                            "region": "nova",
                            "region_id": "nova",
                            "id": "89943db2263e4281b7db8001ce17cdf5"

                        }
                    ],
                    "type": "image",
                    "id": "b2339bfcb20a49a6a44176eaadea5340",
                    "name": "glance"
                },

            ],
            "user": {
                "domain": {
                    "id": "default",
                    "name": "Default"
                },
                "id": "57b05660fff24a8c91ced781d185c2df",
                "name": "admin"
            },
            "audit_ids": [
                "9LzWeP_bTCSaRejb_kg13A"
            ],
            "issued_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    return data


def keystone_tokenV2():

        data = \
            {
                "access": {
                    "token": {
                        "issued_at": "2017-10-24T06:47:51.000000Z",
                        "expires": "2017-10-24T08:47:51.000000Z",
                        "id": Token,
                        "tenant": {
                            "enabled": true,
                            "description": "Bootstrap "
                                           "project for "
                                           "initializing the cloud.",
                            "name": "admin",
                            "id": Tenantid
                        },
                        "audit_ids": [
                            "_KKMw5S3RUCl8SNKwmiDcA"
                        ]
                    },
                    "serviceCatalog": [
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL":
                                        "http://" + MSB_SERVER +
                                        "/api/multicloud-vio/"
                                        "v0/vmware_fake/nova/" + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/nova/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER
                                                   + "/api/multicloud-vio/"
                                                     "v0/vmware_fake/nova/"
                                                   + Tenantid,
                                    "id": "10fd2ceacc994090a96ab3b8541e066e"
                                }
                            ],
                            "type": "compute",
                            "name": "nova"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/neutron",
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/neutron",
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/neutron",
                                    "id": "1bf876c18fd64e4f89cfa3c8a9624864"
                                }
                            ],
                            "type": "network",
                            "name": "neutron"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/cinderv2/"
                                                + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/cinderv2/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER
                                                   + "/api/multicloud-vio/"
                                                     "v0/vmware_fake/cinderv2/"
                                                   + Tenantid,
                                    "id": "70ed007f3aae44288e1851d5ade542ef"
                                }
                            ],
                            "type": "volumev2",
                            "name": "cinderv2"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/cinderv3/"
                                                + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/cinderv3/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/cinderv3/"
                                                   + Tenantid,
                                    "id": "2090cf622a904c1bbc0f500c2f1b1c78"
                                }
                            ],
                            "type": "volumev3",
                            "name": "cinderv3"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER
                                                + "/api/multicloud-vio/"
                                                  "v0/vmware_fake/glance",
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER
                                                 + "/api/multicloud-vio/"
                                                   "v0/vmare_fake/glance",
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/glance",
                                    "id": "25404699d5fc4e1989f421243c0006d1"
                                }
                            ],
                            "type": "image",
                            "name": "glance"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/nova_legacy/"
                                                + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/nova_legacy/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/"
                                                   "nova_legacy/"
                                                   + Tenantid,
                                    "id": "303b4193e0784d0391a2bc318ff27229"
                                }
                            ],
                            "type": "compute_legacy",
                            "name": "nova_legacy"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER
                                                + "/api/multicloud-vio/"
                                                  "v0/vmware_fake/heat-cfn",
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/heat-cfn",
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/heat-cfn",
                                    "id": "1152aa50dd1a4a99be272aa84f910ef6"
                                }
                            ],
                            "type": "cloudformation",
                            "name": "heat-cfn"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/cinder/"
                                                + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/cinder/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/cinder/"
                                                   + Tenantid,
                                    "id": "1cdfe5803856412f9daa3bed79f6e9ac"
                                }
                            ],
                            "type": "volume",
                            "name": "cinder"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/heat/"
                                                + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/heat/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/heat/"
                                                   + Tenantid,
                                    "id": "7eb9b5633c8f431da405192665782392"
                                }
                            ],
                            "type": "orchestration",
                            "name": "heat"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/placement/"
                                                + Tenantid,
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/placement/"
                                                 + Tenantid,
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/placement/"
                                                   + Tenantid,
                                    "id": "9b509d9d5db54f51bbd27d9991586250"
                                }
                            ],
                            "type": "placement",
                            "name": "placement"
                        },
                        {
                            "endpoints_links": [],
                            "endpoints": [
                                {
                                    "adminURL": "http://" + MSB_SERVER +
                                                "/api/multicloud-vio/"
                                                "v0/vmware_fake/identity",
                                    "region": "nova",
                                    "publicURL": "http://" + MSB_SERVER +
                                                 "/api/multicloud-vio/"
                                                 "v0/vmware_fake/identity",
                                    "internalURL": "http://" + MSB_SERVER +
                                                   "/api/multicloud-vio/"
                                                   "v0/vmware_fake/identity",
                                    "id": "62a158d5b28d4fdbb485e8cf6ae5cc92"
                                }
                            ],
                            "type": "identity",
                            "name": "keystone"
                        }
                    ],
                    "user": {
                        "username": "admin",
                        "roles_links": [],
                        "id": "08a03743532f4c64b5e283b15646fd10",
                        "roles": [
                            {
                                "name": "admin"
                            }
                        ],
                        "name": "admin"
                    },
                    "metadata": {
                        "is_admin": 0,
                        "roles": [
                            "cd1ffa75112d47f9ac64a758fa75d688"
                        ]
                    }
                }
            }

        return data


def list_projects(token=None):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data = {
        "projects": [
            {
                "is_domain": "false",
                "description": "Admin Project",
                "links": {
                    "self": "http://127.0.0.1:5000/v3/"
                            "projects/0cf31a5c8da74fe3afb14683f9043f7b"
                },
                "enabled": "true",
                "domain_id": "c049d4ad1dee475db8c3627bef9e916a",
                "parent_id": "c049d4ad1dee475db8c3627bef9e916a",
                "id": Tenantid,
                "name": "admin"
            },
            {
                "is_domain": "false",
                "description": "Bootstrap project for "
                               "initializing the cloud.",
                "links": {
                    "self": "http://127.0.0.1:5000/v3/projects"
                            "/3888e02273224c7a93c961d8dde8094f"
                },
                "enabled": "true",
                "domain_id": "default",
                "parent_id": "default",
                "id": "3888e02273224c7a93c961d8dde8094f",
                "name": "admin"
            },
            {
                "is_domain": "false",
                "description": "Service Project",
                "links": {
                    "self": "http://127.0.0.1:5000/v3/"
                            "projects/e75f80048997438dbc0bfaa822dfdf65"
                },
                "enabled": "true",
                "domain_id": "c049d4ad1dee475db8c3627bef9e916a",
                "parent_id": "c049d4ad1dee475db8c3627bef9e916a",
                "id": "e75f80048997438dbc0bfaa822dfdf65",
                "name": "service"
            }
        ],
        "links": {
            "self": "http://127.0.0.1:5000/v3/projects",
            "next": "null",
            "previous": "null"
        }
    }

    return data


def show_project(token, projectid=""):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data = {
        "project":
            {
                "is_domain": "false", "description": "Admin Project", "links":
                {
                    "self": "https://127.0.0.1:5000/v3/projects"
                            "/9e8a26d207ef454981750e98e42e9aa8"
                },
                "enabled": "true", "id": projectid,
                "parent_id": "e71c537250a74a7a8917904a8ece675c",
                "domain_id": "e71c537250a74a7a8917904a8ece675c",
                "name": "admin"
            }
    }

    return data


# used for keystonev2
def get_tenants():

    data = \
        {
            "tenants": [
                {
                    "id": Tenantid,
                    "name": "admin",
                    "description": "A description ...",
                    "enabled": true
                }
            ],
            "tenants_links": []
        }

    return data


def get_serverdetail(token):

    data = {"servers": []}

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}
    if serverMapps == {}:
        return data
    else:
        tmp = copy.deepcopy(serverMapps)
        for k, v in tmp.iteritems():
            try:
                _serverStatus(k)
            except Exception:
                # deleting
                continue

            server = {
                "OS-DCF:diskConfig": "AUTO",
                "OS-EXT-AZ:availability_zone": "nova",
                "OS-EXT-SRV-ATTR:host": "compute",
                "OS-EXT-SRV-ATTR:hostname": "new-server-test",
                "OS-EXT-SRV-ATTR:hypervisor_hostname": "fake-mini",
                "OS-EXT-SRV-ATTR:instance_name": "instance-00000001",
                "OS-EXT-SRV-ATTR:kernel_id": "",
                "OS-EXT-SRV-ATTR:launch_index": 0,
                "OS-EXT-SRV-ATTR:ramdisk_id": "",
                "OS-EXT-SRV-ATTR:reservation_id": "r-iffothgx",
                "OS-EXT-SRV-ATTR:root_device_name": "/dev/sda",
                "OS-EXT-SRV-ATTR:user_data": "IyEvYmluL2Jh"
                                             "c2gKL2Jpbi9zdQpl"
                                             "Y2hvICJJIGFtIGl"
                                             "uIHlvdSEiCg==",
                "OS-EXT-STS:power_state": 1,
                "OS-EXT-STS:task_state": null,
                "OS-EXT-STS:vm_state": v['status'],
                "OS-SRV-USG:launched_at": "2017-02-14T19:24:43.891568",
                "OS-SRV-USG:terminated_at": null,
                "accessIPv4": "1.2.3.4",
                "accessIPv6": "80fe::",
                "addresses": {
                    "private": [
                        {
                            "OS-EXT-IPS-MAC:mac_addr": "aa:bb:cc:dd:ee:ff",
                            "OS-EXT-IPS:type": "fixed",
                            "addr": "192.168.0.3",
                            "version": 4
                        }
                    ]
                },
                "config_drive": "",
                "created": v['createTime'],
                "description": null,
                "flavor": {
                    "disk": 1,
                    "ephemeral": 0,
                    "extra_specs": {
                        "hw:cpu_model": "SandyBridge",
                        "hw:mem_page_size": "2048",
                        "hw:cpu_policy": "dedicated"
                    },
                    "original_name": "m1.tiny.specs",
                    "ram": 512,
                    "swap": 0,
                    "vcpus": 1
                },
                "hostId": "2091634baaccdc4c5a1d570"
                          "69c833e402921df696b7f970791b12ec6",
                "host_status": "UP",
                "id": k,
                "image": {
                    "id": "70a599e0-31e7-49b7-b260-868f441e862b",
                    "links": [
                        {
                            "href": "http://openstack.example.com/"
                                    "6f70656e737461636b20342065766572/"
                                    "images/70a599e0-31e7-4"
                                    "9b7-b260-868f441e862b",
                            "rel": "bookmark"
                        }
                    ]
                },
                "key_name": null,
                "links": [
                    {
                        "href": "http://openstack.example.com/v2.1"
                                "/6f70656e737461636b20342065766572"
                                "/servers/764e369e-a874-440"
                                "1-b7ce-43e4760888da",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com/"
                                "6f70656e737461636b20342065766572/"
                                "servers/764e369e-a874-4401"
                                "-b7ce-43e4760888da",
                        "rel": "bookmark"
                    }
                ],
                "locked": false,
                "metadata": {
                    "My Server Name": "Apache1"
                },
                "name": v['name'],
                "os-extended-volumes:volumes_attached": [
                    {
                        "delete_on_termination": false,
                        "id": "volume_id1"
                    },
                    {
                        "delete_on_termination": false,
                        "id": "volume_id2"
                    }
                ],
                "progress": 0,
                "security_groups": [
                    {
                        "name": "default"
                    }
                ],
                "status": v['status'].upper(),
                "tags": [],
                "tenant_id": v['tenantid'],
                "updated": "2017-02-14T19:24:43Z",
                "user_id": "fake"
            }

            data['servers'].append(server)
    return data


def get_osaggregates(token):

    data = {
        "aggregates": [
            {
                "availability_zone": "london",
                "created_at": "2016-12-27T23:47:32.911515",
                "deleted": "false",
                "deleted_at": "null",
                "hosts": [
                    "compute"
                ],
                "id": 1,
                "metadata": {
                    "availability_zone": "london"
                },
                "name": "name",
                "updated_at": "null",
                "uuid": "6ba28ba7-f29b-45cc-a30b-6e3a40c2fb14"
            }
        ]
    }
    return data


def get_oshypervisor(token, hyperid=None):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    if hyperid is not None:
        data = {
            "hypervisor":
                {
                    "status": "enabled",
                    "vcpus": 24,
                    "service": {
                        "host": "compute01",
                        "disabled_reason": "null",
                        "id": 12
                    },
                    "vcpus_used": 1,
                    "hypervisor_type": "VMware vCenter Server",
                    "local_gb_used": 1107,
                    "host_ip": "127.0.0.1",
                    "hypervisor_hostname": "domain-c202.22bfc"
                                           "05c-da55-4ba6-ba93-08d9a067138e",
                    "memory_mb_used": 32762,
                    "memory_mb": 98258,
                    "current_workload": 0,
                    "state": "up",
                    "cpu_info": "",
                    "running_vms": 1,
                    "free_disk_gb": 4478,
                    "hypervisor_version": 6000000,
                    "disk_available_least": "null",
                    "local_gb": 5585,
                    "free_ram_mb": 65496,
                    "id": 1
                }

        }
        return data

    data = {
        "hypervisors": [
            {
                "status": "enabled",
                "vcpus": 24,
                "service": {
                    "host": "compute01",
                    "disabled_reason": "null",
                    "id": 12
                },
                "vcpus_used": 1,
                "hypervisor_type": "VMware vCenter Server",
                "local_gb_used": 1107,
                "host_ip": "127.0.0.1",
                "hypervisor_hostname":
                    "domain-c202.22bfc05c-da55-4ba6-ba93-08d9a067138e",
                "memory_mb_used": 32762,
                "memory_mb": 98258,
                "current_workload": 0,
                "state": "up",
                "cpu_info": "",
                "running_vms": 1,
                "free_disk_gb": 4478,
                "hypervisor_version": 6000000,
                "disk_available_least": "null",
                "local_gb": 5585,
                "free_ram_mb": 65496,
                "id": 1
            }
        ]
    }

    return data


def get_servers(token, tenantid=None):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data = {"servers": []}
    for k, v in serverMapps.iteritems():
        server = {"id": k,
                  "links": [
                      {
                          "href": "https://127.0.0.1:8774/v2.1/"
                                  + v['tenantid'] + "/servers/" + k,
                          "ref": "self"
                      },
                      {
                          "href": "https://127.0.0.1:8774/v2.1/"
                                  + v['tenantid'] + "/servers/" + k,
                          "ref": "bookmark"
                      }

                  ],
                  "name": v['name']

                  }
        data['servers'].append(server)

    return data


def show_serverDetail(token, serverid, tenantid=None):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    if serverid not in serverMapps:
        return {
            "error":
                {
                    "message":
                    "instance {0} is not exsit".
                    format(serverid),
                    "code": 404
                }
        }

    try:
        _serverStatus(serverid)
    except ValueError:
        return \
            {
                "error":
                {
                    "message":
                        "instance {0} is not exsit".
                        format(serverid),
                    "code": 404
                }
            }

    data = {
        "server": {
            "OS-EXT-STS:task_state": "null",
            "addresses": {
                "oam_onap_L6dr": [
                    {
                        "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:20:46:79",
                        "version": 4,
                        "addr": "192.168.15.30",
                        "OS-EXT-IPS:type": "fixed"
                    },
                    {
                        "OS-EXT-IPS-MAC:mac_addr": "fa:16:3e:20:46:79",
                        "version": 4,
                        "addr": "127.0.0.1",
                        "OS-EXT-IPS:type": "floating"
                    }
                ]
            },
            "links": [
                {
                    "href": "https://127.0.0.1:8774/v2.1/" +
                            Tenantid + "/servers/" + serverid,
                    "rel": "self"
                },
                {
                    "href": "https://127.0.0.1:8774/" +
                            Tenantid + "/servers/" + serverid,
                    "rel": "bookmark"
                }
            ],
            "image": {
                "id": "0c80630a-eb3a-47c0-950a-facb2721139c",
                "links": [
                    {
                        "href": "https://127.0.0.1:8774/" +
                                Tenantid +
                                "/images/0c80630a"
                                "-eb3a-47c0-950a-facb2721139c",
                        "rel": "bookmark"
                    }
                ]
            },

            "OS-EXT-STS:vm_state": serverMapps[serverid]['status'].lower(),
            "OS-EXT-SRV-ATTR:instance_name": "instance-00000053",
            "OS-SRV-USG:launched_at":
                (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            "flavor": {
                "id": "13",
                "links": [
                    {
                        "href": "https://127.0.0.1:8774/"
                                + Tenantid + "/flavors/13",
                        "rel": "bookmark"
                    }
                ]
            },
            "id": serverid,
            "security_groups": [
                {
                    "name": "default"
                }
            ],
            "user_id": "fb06e6dbedad41a1b78312367f80ae70",
            "OS-DCF:diskConfig": "MANUAL",
            "accessIPv4": "",
            "accessIPv6": "",
            "progress": 0,
            "OS-EXT-STS:power_state": 1,
            "OS-EXT-AZ:availability_zone": "nova",
            "metadata": {},
            "status": serverMapps[serverid]['status'],
            "updated":
                (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            "hostId":
                "5a9fc696507589459e64ba6dfb0ad1570c0952cdd1c184b0b7bdde9a",
            "OS-EXT-SRV-ATTR:host": "compute01",
            "OS-SRV-USG:terminated_at": "null",
            "key_name": "onap_key_L6dr",
            "OS-EXT-SRV-ATTR:hypervisor_hostname":
                "domain-c202.22bfc05c-da55-4ba6-ba93-08d9a067138e",
            "name": "vio-mso",
            "created": serverMapps[serverid]['createTime'],
            "tenant_id": tenantid,
            "os-extended-volumes:volumes_attached": [],
            "config_drive": ""
        }
    }

    return data


def delete_server(token, serverid):

    if token != Token:
        return {"error": {
                        "message": "unauthorization",
                        "code": 401
                         }
                }

    if serverid not in serverMapps:
        return {
            "error": {
                "message":
                "instance {0} is not exsit".format(serverid), "code": 404
                }
        }

    serverMapps[serverid]['turnStatusTime'] = datetime.now()
    serverMapps[serverid]['status'] = "DELETING"

    return {}


def operator_server(token, serverid, action):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    if serverid not in serverMapps:
        return {
            "error": {
                "message":
                "instance {0} is not exsit".format(serverid),
                "code": 404
            }
        }

    try:
        _serverStatus(serverid)
    except ValueError:
        return {
            "error": {
                "message": "instance {0} is not exsit".format(serverid),
                "code": 404
            }
        }

    if action == "os-stop":
        if serverMapps[serverid]['status'] != "ACTIVE":
            return {
                "error": {
                    "message":
                        "Cannot 'stop' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['turnStatusTime'] = datetime.now()
        serverMapps[serverid]['status'] = "POWERING_OFF"

    elif action == "os-start":
        if serverMapps[serverid]['status'] != "SHUTDOWN":
            return {
                "error": {
                    "message":
                        "Cannot 'start' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['turnStatusTime'] = datetime.now()
        serverMapps[serverid]['status'] = "POWERING_ON"

    elif action == "resume":
        if serverMapps[serverid]['status'] != "SUSPENDED":
            return {
                "error": {
                    "message":
                        "Cannot 'resume' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "ACTIVE"

    elif action == "suspend":
        if serverMapps[serverid]['status'] != "ACTIVE":
            return {
                "error": {
                    "message":
                        "Cannot 'suspend' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "SUSPENDED"

    elif action == "unpause":

        if serverMapps[serverid]['status'] != "PAUSED":
            return {
                "error": {
                    "message":
                        "Cannot 'unpause' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "ACTIVE"

    elif action == "pause":
        if serverMapps[serverid]['status'] != "ACTIVE":
            return {
                "error": {
                    "message":
                        "Cannot 'pause' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "PAUSED"

    elif action == "reboot":
        if serverMapps[serverid]['status'] == "ERROR" or \
                        serverMapps[serverid]['status'] == "REBOOTING":
            return {
                "error": {
                    "message":
                        "Cannot 'reboot' instance {0} "
                        "while it is in vm_state {1}".
                        format(serverid, serverMapps[serverid]['status']),
                    "code": 409
                }
            }
        serverMapps[serverid]['turnStatusTime'] = datetime.now()
        serverMapps[serverid]['status'] = "REBOOTING"

    else:
        return {"error": {"message": "unspported action", "code": 405}}

    return {}


def hypervisor_uptime():

    data = {
            "hypervisor": {
                "hypervisor_hostname": "fake-mini",
                "id": 1,
                "state": "up",
                "status": "enabled",
                "uptime": " 08:32:11 up 93 days, 18:25, 12 users,  "
                          "load average: 0.20, 0.12, 0.14"
            }
        }

    return data


def get_flavors(flag):

    data = ""
    if flag == "detail":
        data = {
            "flavors": [
                {
                    "OS-FLV-DISABLED:disabled": false,
                    "disk": 1,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "os-flavor-access:is_public": true,
                    "id": "1",
                    "links": [
                        {
                            "href": "http://openstack.example.com/"
                                    "v2/6f70656e737461636b20342065766572"
                                    "/flavors/1",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/"
                                    "6f70656e737461636b20342065766572"
                                    "/flavors/1",
                            "rel": "bookmark"
                        }
                    ],
                    "name": "m1.tiny",
                    "ram": 512,
                    "swap": "",
                    "vcpus": 1,
                    "rxtx_factor": 1.0
                },
                {
                    "OS-FLV-DISABLED:disabled": false,
                    "disk": 20,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "os-flavor-access:is_public": true,
                    "id": "2",
                    "links": [
                        {
                            "href": "http://openstack.example.com/"
                                    "v2/6f70656e737461636b20342065766572"
                                    "/flavors/2",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com"
                                    "/6f70656e737461636b20342065766572"
                                    "/flavors/2",
                            "rel": "bookmark"
                        }
                    ],
                    "name": "m1.small",
                    "ram": 2048,
                    "swap": "",
                    "vcpus": 1,
                    "rxtx_factor": 1.0
                },
                {
                    "OS-FLV-DISABLED:disabled": false,
                    "disk": 40,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "os-flavor-access:is_public": true,
                    "id": "3",
                    "links": [
                        {
                            "href": "http://openstack.example.com/v2/"
                                    "6f70656e737461636b20342065766572/"
                                    "flavors/3",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/"
                                    "6f70656e737461636b20342065766572/"
                                    "flavors/3",
                            "rel": "bookmark"
                        }
                    ],
                    "name": "m1.medium",
                    "ram": 4096,
                    "swap": "",
                    "vcpus": 2,
                    "rxtx_factor": 1.0
                },
                {
                    "OS-FLV-DISABLED:disabled": false,
                    "disk": 80,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "os-flavor-access:is_public": true,
                    "id": "4",
                    "links": [
                        {
                            "href": "http://openstack.example.com/v2"
                                    "/6f70656e737461636b20342065766572"
                                    "/flavors/4",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/"
                                    "6f70656e737461636b20342065766572"
                                    "/flavors/4",
                            "rel": "bookmark"
                        }
                    ],
                    "name": "m1.large",
                    "ram": 8192,
                    "swap": "",
                    "vcpus": 4,
                    "rxtx_factor": 1.0
                },
                {
                    "OS-FLV-DISABLED:disabled": false,
                    "disk": 160,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "os-flavor-access:is_public": true,
                    "id": "5",
                    "links": [
                        {
                            "href": "http://openstack.example.com/v2/"
                                    "6f70656e737461636b20342065766572/"
                                    "flavors/5",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/"
                                    "6f70656e737461636b20342065766572/"
                                    "flavors/5",
                            "rel": "bookmark"
                        }
                    ],
                    "name": "m1.xlarge",
                    "ram": 16384,
                    "swap": "",
                    "vcpus": 8,
                    "rxtx_factor": 1.0
                },
                {
                    "OS-FLV-DISABLED:disabled": false,
                    "disk": 1,
                    "OS-FLV-EXT-DATA:ephemeral": 0,
                    "os-flavor-access:is_public": true,
                    "id": "6",
                    "links": [
                        {
                            "href": "http://openstack.example.com/"
                                    "v2/6f70656e737461636b20342065766572"
                                    "/flavors/6",
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/"
                                    "6f70656e737461636b20342065766572"
                                    "/flavors/6",
                            "rel": "bookmark"
                        }
                    ],
                    "name": "m1.tiny.specs",
                    "ram": 512,
                    "swap": "",
                    "vcpus": 1,
                    "rxtx_factor": 1.0
                }
            ]
        }
    else:
        data = {
            "flavor": {
                "OS-FLV-DISABLED:disabled": "false",
                "disk": 1,
                "OS-FLV-EXT-DATA:ephemeral": 0,
                "os-flavor-access:is_public": "true",
                "id": flag,
                "links": [
                    {
                        "href": "http://openstack.example.com/"
                                "v2/6f70656e737461636b20342065766572"
                                "/flavors/1",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com/"
                                "6f70656e737461636b20342065766572"
                                "/flavors/1",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.tiny",
                "ram": 512,
                "swap": "",
                "vcpus": 1,
                "rxtx_factor": 1.0
            }
        }

    return data


def list_flavors():

    data = {
        "flavors": [
            {
                "id": "1",
                "links": [
                    {
                        "href": "http://openstack.example.com/"
                                "v2/6f70656e737461636b20342065766572"
                                "/flavors/1",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/1",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.tiny"
            },
            {
                "id": "2",
                "links": [
                    {
                        "href": "http://openstack.example.com/v2"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/2",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com/"
                                "6f70656e737461636b20342065766572"
                                "/flavors/2",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.small"
            },
            {
                "id": "3",
                "links": [
                    {
                        "href": "http://openstack.example.com/v2"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/3",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com/"
                                "6f70656e737461636b20342065766572"
                                "/flavors/3",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.medium"
            },
            {
                "id": "4",
                "links": [
                    {
                        "href": "http://openstack.example.com/v2"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/4",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com/"
                                "6f70656e737461636b20342065766572"
                                "/flavors/4",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.large"
            },
            {
                "id": "5",
                "links": [
                    {
                        "href": "http://openstack.example.com/v2"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/5",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/5",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.xlarge"
            },
            {
                "id": "6",
                "links": [
                    {
                        "href": "http://openstack.example.com/"
                                "v2/6f70656e737461636b20342065766572"
                                "/flavors/6",
                        "rel": "self"
                    },
                    {
                        "href": "http://openstack.example.com"
                                "/6f70656e737461636b20342065766572"
                                "/flavors/6",
                        "rel": "bookmark"
                    }
                ],
                "name": "m1.tiny.specs"
            }
        ]
    }

    return data


def create_instance(token, json=None):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    try:
        name = json['server']['name']

    except Exception:
        return {"error": {"message": "invalidate data", "code": 403}}

    # It's safe to using inner vm id,
    # Avoid data sharing in multiprocess.
    uid = InitialServer
    data = {
        "server": {
            "id": uid,
            "links": [
                {
                    "href": "http://openstack.example.com/v2/"
                            + Tenantid + "/servers/" + uid,
                    "rel": "self"
                },
                {
                    "href": "http://openstack.example.com/"
                            + Tenantid + "/servers/" + uid,
                    "rel": "bookmark"
                }
            ],
            "name": name
        }
    }

    serverMapps[uid] = \
        {
        "name": name,
        "tenantid": Tenantid,
        "status": "BUILDING",
        'createTime': (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "turnStatusTime": datetime.now()
        }

    return data


def _serverStatus(serverid):

    startTime = serverMapps[serverid]['turnStatusTime']
    currentTime = datetime.now()
    print(currentTime - startTime)
    if currentTime - startTime >= timedelta(seconds=10):
        if serverMapps[serverid]['status'] == "SPAWNING" \
                or serverMapps[serverid]['status'] == "BUILDING":
            serverMapps[serverid]['status'] = "ACTIVE"
        elif serverMapps[serverid]['status'] == "DELETING":
            return
        elif serverMapps[serverid]['status'] == "POWERING_OFF":
            serverMapps[serverid]['status'] = "SHUTDOWN"
        elif serverMapps[serverid]['status'] == "POWERING_ON":
            serverMapps[serverid]['status'] = "ACTIVE"

        elif serverMapps[serverid]['status'] == "REBOOTING":
            serverMapps[serverid]['status'] = "ACTIVE"
        else:
            pass
    elif timedelta(seconds=5) \
            <= currentTime - startTime < timedelta(seconds=10):
        if serverMapps[serverid]['status'] == "BUILDING":
            serverMapps[serverid]['status'] = "SPAWNING"
    else:
        pass


def neutron_version(token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data = {
        "versions": [
            {
                "status": "CURRENT",
                "id": "v2.0",
                "links": [
                    {
                        "href": "http://" + MSB_SERVER
                                + "/api/multicloud-vio/"
                                  "v0/vmware_fake/neutron",
                        "rel": "self"
                    }
                ]
            }
        ]
    }
    return data


def neutron_detail(token, netid):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data = {
        "network": {
            "provider:physical_network": "dvs-231",
            "updated_at": "2017-09-05T11:00:28Z",
            "revision_number": 5,
            "port_security_enabled": true,
            "id": netid,
            "router:external": false,
            "availability_zone_hints": [],
            "availability_zones": [
                "default"
            ],
            "ipv4_address_scope": null,
            "shared": false,
            "project_id": Tenantid,
            "status": "ACTIVE",
            "subnets": [
                "df5993f1-1dde-4b38-b640-f8264ab4c95a"
            ],
            "description": "",
            "tags": [],
            "ipv6_address_scope": null,
            "provider:segmentation_id": 0,
            "name": "internal",
            "admin_state_up": true,
            "tenant_id": Tenantid,
            "created_at": "2017-09-05T10:59:29Z",
            "provider:network_type": "flat"
        }
    }
    return data


def network_list(token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data = {
        "networks": [
            {
                "provider:physical_network": "dvportgroup-233",
                "updated_at": "2017-09-06T05:26:23Z",
                "revision_number": 11,
                "port_security_enabled": true,
                "id": "20bc6595-282d-4406-be43-017651a4cbe9",
                "router:external": true,
                "availability_zone_hints": [],
                "availability_zones": [],
                "ipv4_address_scope": null,
                "shared": true,
                "project_id": Tenantid,
                "status": "ACTIVE",
                "subnets": [
                    "9251a816-f1f0-4332-864d-ca32fe6d44bb"
                ],
                "description": "",
                "tags": [],
                "ipv6_address_scope": null,
                "is_default": false,
                "provider:segmentation_id": 0,
                "name": "public",
                "admin_state_up": true,
                "tenant_id": Tenantid,
                "created_at": "2017-09-05T10:52:20Z",
                "provider:network_type": "portgroup"
            },
            {
                "provider:physical_network": "dvs-231",
                "updated_at": "2017-09-05T11:00:28Z",
                "revision_number": 5,
                "port_security_enabled": true,
                "id": "2dde80bf-2923-4466-baec-6b1e5c670366",
                "router:external": false,
                "availability_zone_hints": [],
                "availability_zones": [
                    "default"
                ],
                "ipv4_address_scope": null,
                "shared": false,
                "project_id": Tenantid,
                "status": "ACTIVE",
                "subnets": [
                    "df5993f1-1dde-4b38-b640-f8264ab4c95a"
                ],
                "description": "",
                "tags": [],
                "ipv6_address_scope": null,
                "provider:segmentation_id": 0,
                "name": "internal",
                "admin_state_up": true,
                "tenant_id": Tenantid,
                "created_at": "2017-09-05T10:59:29Z",
                "provider:network_type": "flat"
            }
        ]
    }

    return data


def image_detail():

    data = {
        "status": "active",
        "name": "cirros-0.3.2-x86_64-disk",
        "tags": [],
        "container_format": "bare",
        "created_at": "2014-05-05T17:15:10Z",
        "disk_format": "qcow2",
        "updated_at": "2014-05-05T17:15:11Z",
        "visibility": "public",
        "self": "/v2/images/1bea47ed-f6a9-463b-b423-14b9cca9ad27",
        "min_disk": 0,
        "protected": "false",
        "id": Imageid,
        "file": "/v2/images/1bea47ed-f6a9-463b-b423-14b9cca9ad27/file",
        "checksum": "64d7c1cd2b6f60c92c14662941cb7913",
        "owner": "5ef70662f8b34079a6eddb8da9d75fe8",
        "size": 13167616,
        "min_ram": 0,
        "schema": "/v2/schemas/image",
        "virtual_size": "null"
    }

    return data


def upload_image(req):

    data = {
        "status": "active",
        "name": req.get('name'),
        "tags": [],
        "container_format": req.get('container_format'),
        "created_at": "2014-05-05T17:15:10Z",
        "disk_format": req.get('disk_format'),
        "updated_at": "2014-05-05T17:15:11Z",
        "visibility": req.get('visibility'),
        "self": "/v2/images/1bea47ed-f6a9-463b-b423-14b9cca9ad27",
        "min_disk": 0,
        "protected": "false",
        "id": Imageid,
        "file": "/v2/images/1bea47ed-f6a9-463b-b423-14b9cca9ad27/file",
        "checksum": "64d7c1cd2b6f60c92c14662941cb7913",
        "owner": "5ef70662f8b34079a6eddb8da9d75fe8",
        "size": 13167616,
        "min_ram": 0,
        "schema": req.get('schema'),
        "virtual_size": "null"
    }

    return data


def list_image():

    data = {
        "images": [
            {
                "status": "active",
                "name": "cirros-0.3.2-x86_64-disk",
                "tags": [],
                "container_format": "bare",
                "created_at": "2014-05-05T17:15:10Z",
                "disk_format": "qcow2",
                "updated_at": "2014-05-05T17:15:11Z",
                "visibility": "public",
                "self": "/v2/images/1bea47ed-f6a9-463b-b423-14b9cca9ad27",
                "min_disk": 0,
                "protected": "false",
                "id": Imageid,
                "file": "/v2/images/1bea47ed-f6a9-463b-"
                        "b423-14b9cca9ad27/file",
                "checksum": "64d7c1cd2b6f60c92c14662941cb7913",
                "owner": "5ef70662f8b34079a6eddb8da9d75fe8",
                "size": 13167616,
                "min_ram": 0,
                "schema": "/v2/schemas/image",
                "virtual_size": "null"

            }
        ],
        "schema": "/v2/schemas/images",
        "first": "/v2/images"
    }

    return data


def image_version():

    data = {
        "versions": [
            {
                "id": "v2.6",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "EXPERIMENTAL"
            },
            {
                "id": "v2.5",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "CURRENT"
            },
            {
                "id": "v2.4",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "SUPPORTED"
            },
            {
                "id": "v2.3",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "SUPPORTED"
            },
            {
                "id": "v2.2",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "SUPPORTED"
            },
            {
                "id": "v2.1",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "SUPPORTED"
            },
            {
                "id": "v2.0",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v2/",
                        "rel": "self"
                    }
                ],
                "status": "SUPPORTED"
            },
            {
                "id": "v1.1",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v1/",
                        "rel": "self"
                    }
                ],
                "status": "DEPRECATED"
            },
            {
                "id": "v1.0",
                "links": [
                    {
                        "href": "http://glance.openstack.example.org/v1/",
                        "rel": "self"
                    }
                ],
                "status": "DEPRECATED"
            }
        ]
    }
    return data


def image_schema():

    data = {
        "additionalProperties": {
            "type": "string"
        },
        "links": [
            {
                "href": "{self}",
                "rel": "self"
            },
            {
                "href": "{file}",
                "rel": "enclosure"
            },
            {
                "href": "{schema}",
                "rel": "describedby"
            }
        ],
        "name": "image",
        "properties": {
            "architecture": {
                "description": "Operating system "
                               "architecture as specified in "
                               "https://docs.openstack.org/"
                               "python-glanceclient"
                               "/latest/cli/property-keys.html",
                "is_base": false,
                "type": "string"
            },
            "checksum": {
                "description": "md5 hash of image contents.",
                "maxLength": 32,
                "readOnly": true,
                "type": [
                    "null",
                    "string"
                ]
            },
            "container_format": {
                "description": "Format of the container",
                "enum": [
                    null,
                    "ami",
                    "ari",
                    "aki",
                    "bare",
                    "ovf",
                    "ova",
                    "docker"
                ],
                "type": [
                    "null",
                    "string"
                ]
            },
            "created_at": {
                "description": "Date and time of image registration",
                "readOnly": true,
                "type": "string"
            },
            "direct_url": {
                "description": "URL to access the image "
                               "file kept in external store",
                "readOnly": true,
                "type": "string"
            },
            "disk_format": {
                "description": "Format of the disk",
                "enum": [
                    null,
                    "ami",
                    "ari",
                    "aki",
                    "vhd",
                    "vhdx",
                    "vmdk",
                    "raw",
                    "qcow2",
                    "vdi",
                    "iso",
                    "ploop"
                ],
                "type": [
                    "null",
                    "string"
                ]
            },
            "file": {
                "description": "An image file url",
                "readOnly": true,
                "type": "string"
            },
            "id": {
                "description": "An identifier for the image",
                "pattern": "^([0-9a-fA-F]){8}-"
                           "([0-9a-fA-F]){4}-([0-9a-fA-F])"
                           "{4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$",
                "type": "string"
            },
            "instance_uuid": {
                "description": "Metadata which can be used to "
                               "record which instance this image is "
                               "associated with. (Informational only, "
                               "does not create an instance snapshot.)",
                "is_base": false,
                "type": "string"
            },
            "kernel_id": {
                "description": "ID of image stored in Glance that "
                               "should be used as the kernel "
                               "when booting an AMI-style image.",
                "is_base": false,
                "pattern": "^([0-9a-fA-F]){8}-([0-9a-fA-F]){4}"
                           "-([0-9a-fA-F]){4}-([0-9a-fA-F]){4}"
                           "-([0-9a-fA-F]){12}$",
                "type": [
                    "null",
                    "string"
                ]
            },
            "locations": {
                "description": "A set of URLs to access "
                               "the image file kept in external store",
                "items": {
                    "properties": {
                        "metadata": {
                            "type": "object"
                        },
                        "url": {
                            "maxLength": 255,
                            "type": "string"
                        }
                    },
                    "required": [
                        "url",
                        "metadata"
                    ],
                    "type": "object"
                },
                "type": "array"
            },
            "min_disk": {
                "description": "Amount of disk space "
                               "(in GB) required to boot image.",
                "type": "integer"
            },
            "min_ram": {
                "description": "Amount of ram "
                               "(in MB) required to boot image.",
                "type": "integer"
            },
            "name": {
                "description": "Descriptive name for the image",
                "maxLength": 255,
                "type": [
                    "null",
                    "string"
                ]
            },
            "os_distro": {
                "description": "Common name of operating "
                               "system distribution as specified in "
                               "https://docs.openstack.org/"
                               "python-glanceclient"
                               "/latest/cli/property-keys.html",
                "is_base": false,
                "type": "string"
            },
            "os_version": {
                "description": "Operating system "
                               "version as specified by the distributor",
                "is_base": false,
                "type": "string"
            },
            "owner": {
                "description": "Owner of the image",
                "maxLength": 255,
                "type": [
                    "null",
                    "string"
                ]
            },
            "protected": {
                "description": "If true, image will not be deletable.",
                "type": "boolean"
            },
            "ramdisk_id": {
                "description": "ID of image stored "
                               "in Glance that should be "
                               "used as the ramdisk when "
                               "booting an AMI-style image.",
                "is_base": false,
                "pattern": "^([0-9a-fA-F]){8}-"
                           "([0-9a-fA-F]){4}-([0-9a-fA-F])"
                           "{4}-([0-9a-fA-F]){4}-([0-9a-fA-F]){12}$",
                "type": [
                    "null",
                    "string"
                ]
            },
            "schema": {
                "description": "An image schema url",
                "readOnly": true,
                "type": "string"
            },
            "self": {
                "description": "An image self url",
                "readOnly": true,
                "type": "string"
            },
            "size": {
                "description": "Size of image file in bytes",
                "readOnly": true,
                "type": [
                    "null",
                    "integer"
                ]
            },
            "status": {
                "description": "Status of the image",
                "enum": [
                    "queued",
                    "saving",
                    "active",
                    "killed",
                    "deleted",
                    "pending_delete",
                    "deactivated"
                ],
                "readOnly": true,
                "type": "string"
            },
            "tags": {
                "description": "List of strings related to the image",
                "items": {
                    "maxLength": 255,
                    "type": "string"
                },
                "type": "array"
            },
            "updated_at": {
                "description": "Date and time of the "
                               "last image modification",
                "readOnly": true,
                "type": "string"
            },
            "virtual_size": {
                "description": "Virtual size of image in bytes",
                "readOnly": true,
                "type": [
                    "null",
                    "integer"
                ]
            },
            "visibility": {
                "description": "Scope of image accessibility",
                "enum": [
                    "public",
                    "private"
                ],
                "type": "string"
            }
        }
    }

    return data


# heat stack
STACK_ID = "3095aefc-09fb-4bc7-b1f0-f21a304e864c"
STACK_NAME = "simple_stack"


def getAllStacks(token):
    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    data =  \
        {
            "stacks": [
                {
                    "creation_time": "2014-06-03T20:59:46Z",
                    "deletion_time": null,
                    "description": "sample stack",
                    "id": STACK_ID,
                    "links": [
                        {
                            "href": "http://" + MSB_SERVER + "/"
                                    + API_NAMESPACE + "/"
                                    + Tenantid + "/stacks/" +
                                    STACK_NAME + "/" + STACK_ID,
                            "rel": "self"
                        }
                    ],
                    "parent": null,
                    "stack_name": STACK_NAME,
                    "stack_owner": null,
                    "stack_status": "CREATE_COMPLETE",
                    "stack_status_reason":
                        "Stack CREATE completed successfully",
                    "stack_user_project_id": Tenantid,
                    "tags": null,
                    "updated_time": null
                }
            ]
        }

    return data


def createStack(stack_name, token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    global STACK_NAME
    STACK_NAME = stack_name

    data = {
            "stack": {
                "id": STACK_ID,
                "links": [
                    {
                        "href": "http://" + MSB_SERVER + "/"
                                + API_NAMESPACE + "/"
                                + Tenantid + "/stacks/" +
                                stack_name + "/" + STACK_ID,
                        "rel": "self"
                    }
                ]
            }
        }

    return data


def createStackPreview(stack_name, token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    global STACK_NAME
    STACK_NAME = stack_name

    data =  \
        {
            "stack": {
                "capabilities": [],
                "creation_time": "2017-10-31T15:12:36Z",
                "deletion_time": null,
                "description": "HOT template for Nova Server resource.\n",
                "disable_rollback": true,
                "id": "None",
                "links": [
                    {
                        "href": "http://" + MSB_SERVER + "/" +
                                API_NAMESPACE + "/"
                                + Tenantid + "/stacks/" +
                                STACK_NAME + "/None",
                        "rel": "self"
                    }
                ],
                "notification_topics": [],
                "outputs": [],
                "parameters": {
                    "OS::project_id": Tenantid,
                    "OS::stack_id": "None",
                    "OS::stack_name": "teststack",
                    "admin_user": "cloud-user",
                    "flavor": "m1.small",
                    "image": "F20-cfg",
                    "key_name": "heat_key",
                    "server_name": "MyServer"
                },
                "parent": null,
                "resources": [
                    {
                        "attributes": {},
                        "description": "",
                        "metadata": {},
                        "physical_resource_id": "",
                        "properties": {
                            "description": "Ping and SSH",
                            "name": "the_sg",
                            "rules": [
                                {
                                    "direction": "ingress",
                                    "ethertype": "IPv4",
                                    "port_range_max": null,
                                    "port_range_min": null,
                                    "protocol": "icmp",
                                    "remote_group_id": null,
                                    "remote_ip_prefix": null,
                                    "remote_mode": "remote_ip_prefix"
                                },
                                {
                                    "direction": "ingress",
                                    "ethertype": "IPv4",
                                    "port_range_max": 65535,
                                    "port_range_min": 1,
                                    "protocol": "tcp",
                                    "remote_group_id": null,
                                    "remote_ip_prefix": null,
                                    "remote_mode": "remote_ip_prefix"
                                },
                                {
                                    "direction": "ingress",
                                    "ethertype": "IPv4",
                                    "port_range_max": 65535,
                                    "port_range_min": 1,
                                    "protocol": "udp",
                                    "remote_group_id": null,
                                    "remote_ip_prefix": null,
                                    "remote_mode": "remote_ip_prefix"
                                }
                            ]
                        },
                        "required_by": [
                            "server1"
                        ],
                        "resource_action": "INIT",
                        "resource_identity": {
                            "path": "/resources/the_sg_res",
                            "stack_id": "None",
                            "stack_name": "teststack",
                            "tenant": Tenantid
                        },
                        "resource_name": "the_sg_res",
                        "resource_status": "COMPLETE",
                        "resource_status_reason": "",
                        "resource_type": "OS::Neutron::SecurityGroup",
                        "stack_identity": {
                            "path": "",
                            "stack_id": "None",
                            "stack_name": "teststack",
                            "tenant": Tenantid
                        },
                        "stack_name": STACK_NAME,
                        "updated_time": "2017-10-31T15:12:36Z"
                    },
                    {
                        "attributes": {
                            "accessIPv4": "",
                            "accessIPv6": "",
                            "addresses": "",
                            "console_urls": "",
                            "first_address": "",
                            "instance_name": "",
                            "name": "MyServer",
                            "networks": "",
                            "show": ""
                        },
                        "description": "",
                        "metadata": {},
                        "physical_resource_id": "",
                        "properties": {
                            "admin_pass": null,
                            "admin_user": "cloud-user",
                            "availability_zone": null,
                            "block_device_mapping": null,
                            "config_drive": null,
                            "diskConfig": null,
                            "flavor": "m1.small",
                            "flavor_update_policy": "RESIZE",
                            "image": "F20-cfg",
                            "image_update_policy": "REPLACE",
                            "key_name": "heat_key",
                            "metadata": {
                                "ha_stack": "None"
                            },
                            "name": "MyServer",
                            "networks": [
                                {
                                    "fixed_ip": null,
                                    "network": "private",
                                    "port": null,
                                    "uuid": null
                                }
                            ],
                            "personality": {},
                            "reservation_id": null,
                            "scheduler_hints": null,
                            "security_groups": [
                                "None"
                            ],
                            "software_config_transport": "POLL_SERVER_CFN",
                            "user_data": "",
                            "user_data_format": "HEAT_CFNTOOLS"
                        },
                        "required_by": [],
                        "resource_action": "INIT",
                        "resource_identity": {
                            "path": "/resources/hello_world",
                            "stack_id": "None",
                            "stack_name": "teststack",
                            "tenant": Tenantid
                        },
                        "resource_name": "hello_world",
                        "resource_status": "COMPLETE",
                        "resource_status_reason": "",
                        "resource_type": "OS::Nova::Server",
                        "stack_identity": {
                            "path": "",
                            "stack_id": "None",
                            "stack_name": "teststack",
                            "tenant": Tenantid
                        },
                        "stack_name": "teststack",
                        "updated_time": "2017-10-31T15:12:36Z"
                    }
                ],
                "stack_name": STACK_NAME,
                "stack_owner": null,
                "tags": null,
                "template_description":
                    "HOT template for Nova Server resource.\n",
                "timeout_mins": null,
                "updated_time": null
            }
        }

    return data


def deleteStack(stack_id, token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    if stack_id != STACK_ID:
        return {"error": {"message": "stack not found", "code": 404}}

    return ""


def showStackByID(stack_id, stack_name, token):
    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}
    if stack_id != STACK_ID or stack_name != STACK_NAME:
        return {"error": {"message": "stack not found", "code": 404}}
    else:
        return showStack(stack_name, token)


def showStack(stack_name, token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    if stack_name != STACK_NAME:
        return {"error": {"message": "stack not found", "code": 404}}

    data = \
        {
            "stack": {
                "capabilities": [],
                "creation_time": "2014-06-03T20:59:46Z",
                "deletion_time": null,
                "description": "sample stack",
                "disable_rollback": true,
                "id": STACK_ID,
                "links": [
                    {
                        "href": "http://" + MSB_SERVER + "/"
                                + API_NAMESPACE + "/"
                                + Tenantid + "/stacks/" + STACK_NAME
                                + "/"+STACK_ID,
                        "rel": "self"
                    }
                ],
                "notification_topics": [],
                "outputs": [],
                "parameters": {
                    "OS::project_id": Tenantid,
                    "OS::stack_id": STACK_ID,
                    "OS::stack_name": STACK_NAME
                },
                "parent": null,
                "stack_name": STACK_NAME,
                "stack_owner": "simple_username",
                "stack_status": "CREATE_COMPLETE",
                "stack_status_reason": "Stack CREATE completed successfully",
                "stack_user_project_id": Tenantid,
                "tags": null,
                "template_description": "sample stack",
                "timeout_mins": null,
                "updated_time": null
            }
        }

    return data


def getStackResource(stack_id, token):

    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}

    if stack_id != STACK_ID:
        return {"error": {"message": "stack not found", "code": 404}}

    data = \
        {
            "code": "302 Found",
            "message": "The resource was found at <a "
                       "href=\"http://127.0.0.1:8004/"
                       "v1/369166a68a3a49b78b4e138531556e55"
                       "/stacks/s1/"
                       "da778f26-6d25-4634-9531-d438188e48fd\">"
                       "http://127.0.0.1:8004/v1/"
                       "369166a68a3a49b78b4e138531556e55/stacks"
                       "/s1/da778f26-6d25-4634-9531-d438188e48fd</a>;\n"
                       "you should be redirected automatically.\n\n",
            "title": "Found"
        }

    return data
