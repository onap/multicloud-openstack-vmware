
from vio.pub.config.config import MSB_SERVICE_PORT
from vio.pub.config.config import MSB_SERVICE_IP

from datetime import datetime
from datetime import timedelta

MSB_SERVER = MSB_SERVICE_IP+":"+MSB_SERVICE_PORT

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
         "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"


ServerStatus = "ACTIVE"
ServerId = "ed0f2291-2d54-418a-b14e-f7ffa28b67b4"
TenatId = "c049d4ad1dee475db8c3627bef9e916a"




def keystoneVersion(vimid):
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
                    "href": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/fake/"+vimid+"/identity/v3",
                    "rel": "self"
                }
            ]
        }

    }

    data['version']['update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    return data



def keystoneToken(teanatid=None,vimid=None):

    data=  {
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
            "expires_at": (datetime.now()+timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
            "project": {
                "domain": {
                    "id": "c049d4ad1dee475db8c3627bef9e916a",
                    "name": "local"
                },
                "id": TenatId,
                "name": "admin"
            },
        "catalog":[
            {
                "endpoints":[
                {  "url": "http://"+MSB_SERVER+"/api/multicloud-vio/v0/fake/"+vimid+"/cinder/"+TenatId,
                        "interface": "admin",
                        "region": "nova",
                        "region_id": "nova",
                        "id": "89943db2263e4281b7db8001ce17cdf5"
                },
                ],
                "type": "volume",
                "id": "3e4941704e9941a582b157ac7203ec1b",
                "name": "cinder"
            },

            {
                "endpoints": [
                {
                    "url": "http://"+MSB_SERVER+"/api/multicloud-vio/v0/fake/"+vimid+"/neutron/"+TenatId,
                    "interface": "admin",
                    "region": "nova",
                    "region_id": "nova",
                    "id": "89943db2263e4281b7db8001ce17cdf5"
                },
                ],
                "type": "network",
                "id": "5ef5f5a07e7848bf8f5882785a91177a",
                "name": "neutron"
            },
            {
                "endpoints": [
                {
                    "url": "http://"+MSB_SERVER+"/api/multicloud-vio/v0/fake/"+vimid+"/identity",
                    "interface": "admin",
                    "region": "nova",
                    "region_id": "nova",
                    "id": "89943db2263e4281b7db8001ce17cdf5"},
            ],
                "type": "identity",
                "id": "915d109fadcd40e498f3412f317169c6",
                "name": "keystone"
            },

            {
                "endpoints": [
                    {
                        "url": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/fake/"+vimid+"/heat/"+TenatId,
                        "interface": "admin",
                        "region": "nova",
                        "region_id": "nova",
                        "id": "89943db2263e4281b7db8001ce17cdf5"},
                ],
                "type": "orchestration",
                "id": "9a6ce7f797ad48f68b46dc11dbc1258d",
                "name": "heat"

            },
            {
                "endpoints": [
                    {
                        "url": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/fake/"+vimid+"/nova/"+TenatId,
                        "interface": "admin",
                        "region": "nova",
                        "region_id": "nova",
                        "id": "89943db2263e4281b7db8001ce17cdf5"},
                ],
                "type": "compute",
                "id": "a99dcae3c15e492db80e9e1994306b6d",
                "name": "nova"
            },

            {
                "endpoints": [
                    {
                        "url": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/fake/"+vimid+"/glance",
                        "interface": "admin",
                        "region": "nova",
                        "region_id": "nova",
                        "id": "89943db2263e4281b7db8001ce17cdf5"},
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




def ListProjects(token=None):
    if token != Token:
        return {"error":{"message":"unauthorization","code":401}}



    data = {
                "projects": [
                    {
                        "is_domain": "false",
                        "description": "Admin Project",
                        "links": {
                            "self": "http://10.154.9.82:5000/v3/projects/0cf31a5c8da74fe3afb14683f9043f7b"
                        },
                        "enabled": "true",
                        "domain_id": "c049d4ad1dee475db8c3627bef9e916a",
                        "parent_id": "c049d4ad1dee475db8c3627bef9e916a",
                        "id": TenatId,
                        "name": "admin"
                    },
                    {
                        "is_domain": "false",
                        "description": "Bootstrap project for initializing the cloud.",
                        "links": {
                            "self": "http://10.154.9.82:5000/v3/projects/3888e02273224c7a93c961d8dde8094f"
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
                            "self": "http://10.154.9.82:5000/v3/projects/e75f80048997438dbc0bfaa822dfdf65"
                        },
                        "enabled": "true",
                        "domain_id": "c049d4ad1dee475db8c3627bef9e916a",
                        "parent_id": "c049d4ad1dee475db8c3627bef9e916a",
                        "id": "e75f80048997438dbc0bfaa822dfdf65",
                        "name": "service"
                    }
                ],
                "links": {
                    "self": "http://10.154.9.82:5000/v3/projects",
                    "next": "null",
                    "previous": "null"
                }
            }

    return data


def showProject(token,projectid=""):
    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}


    data = {
            "project":
                {
                    "is_domain": "false", "description": "Admin Project", "links":
                    {
                        "self": "https://10.154.2.225:5000/v3/projects/9e8a26d207ef454981750e98e42e9aa8"
                    },
                    "enabled": "true", "id": projectid,
                    "parent_id": "e71c537250a74a7a8917904a8ece675c", "domain_id": "e71c537250a74a7a8917904a8ece675c", "name": "admin"
                }
            }

    return data




def GetOSHypervisor(token):
    if token != Token:
        return {"error":{"message":"unauthorization","code":401}}


    data =  {
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
                    "host_ip": "10.154.9.83",
                    "hypervisor_hostname": "domain-c202.22bfc05c-da55-4ba6-ba93-08d9a067138e",
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




def getServers(token,tenantid=None):


    if token != Token:
        return {"error":{"message":"unauthorization","code":401}}



    data = {
        "servers": [

            {
                "id": ServerId,
                "links": [
                    {
                        "href": "https://10.154.2.225:8774/v2.1/"+tenantid+"/servers/"+ServerId,
                        "rel": "self"
                    },
                    {
                        "href": "https://10.154.2.225:8774/"+tenantid+"/servers/"+ServerId,
                        "rel": "bookmark"
                    }
                ],
                "name": "vio-mso"
            },

        ]
    }


    return data


def showServerDetail(token,serverid,tenantid=None):
    if token != Token:
        return {"error":{"message":"unauthorization","code":401}}

    if serverid != ServerId:
        return {"error": {"message":"instance {0} is not exsit".format(serverid),"code":404}}


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
                        "addr": "10.154.9.70",
                        "OS-EXT-IPS:type": "floating"
                    }
                ]
            },
            "links": [
                {
                    "href": "https://10.154.2.225:8774/v2.1/"+TenatId+"/servers/ed0f2291-2d54-418a-b14e-f7ffa28b67b4",
                    "rel": "self"
                },
                {
                    "href": "https://10.154.2.225:8774/"+TenatId+"/servers/ed0f2291-2d54-418a-b14e-f7ffa28b67b4",
                    "rel": "bookmark"
                }
            ],
            "image": {
                "id": "0c80630a-eb3a-47c0-950a-facb2721139c",
                "links": [
                    {
                        "href": "https://10.154.2.225:8774/"+TenatId+"/images/0c80630a-eb3a-47c0-950a-facb2721139c",
                        "rel": "bookmark"
                    }
                ]
            },
            "OS-EXT-STS:vm_state": ServerStatus.lower(),
            "OS-EXT-SRV-ATTR:instance_name": "instance-00000053",
            "OS-SRV-USG:launched_at": "2017-08-27T10:30:53.000000",
            "flavor": {
                "id": "13",
                "links": [
                    {
                        "href": "https://10.154.2.225:8774/"+TenatId+"/flavors/13",
                        "rel": "bookmark"
                    }
                ]
            },
            "id": "ed0f2291-2d54-418a-b14e-f7ffa28b67b4",
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
            "status": ServerStatus,
            "updated": "2017-08-27T10:30:53Z",
            "hostId": "5a9fc696507589459e64ba6dfb0ad1570c0952cdd1c184b0b7bdde9a",
            "OS-EXT-SRV-ATTR:host": "compute01",
            "OS-SRV-USG:terminated_at": "null",
            "key_name": "onap_key_L6dr",
            "OS-EXT-SRV-ATTR:hypervisor_hostname": "domain-c202.22bfc05c-da55-4ba6-ba93-08d9a067138e",
            "name": "vio-mso",
            "created": "2017-08-27T10:30:33Z",
            "tenant_id": tenantid,
            "os-extended-volumes:volumes_attached": [],
            "config_drive": ""
        }
    }

    return data



def deleteServer(token,serverid):
    if token != Token:
        return {"error": {"message":"unauthorization","code":401}}

    if serverid != ServerId:
        return {"error": {"message": "instance {0} is not exsit".format(serverid), "code": 404}}

    return {}


def operator_server(token,serverid,action):
    if token != Token:
        return {"error": {"message":"unauthorization","code":401}}

    if serverid != ServerId:
        return {"error": {"message":"instance {0} is not exsit".format(serverid),"code":404}}

    global  ServerStatus

    if action == "os-stop":
        if ServerStatus != "ACTIVE":
            return {
                "error": {
                "message": "Cannot 'start' instance {0} while it is in vm_state {1}".format(serverid,ServerStatus),
                "code": 409
                }
            }

        ServerStatus = "SHUTDOWN"
    elif action == "os-start":
        if ServerStatus != "SHUTDOWN":
            return {
                "error": {
                    "message": "Cannot 'shutdown' instance {0} while it is in vm_state {1}".format(serverid,ServerStatus),
                    "code": 409
                }
            }

        ServerStatus = "ACTIVE"


    elif action == "resume":
        if ServerStatus != "SUSPENDED":
            return {
                "error": {
                    "message": "Cannot 'resume' instance {0} while it is in vm_state {1}".format(serverid,ServerStatus),
                    "code": 409
                }
            }

        ServerStatus = "ACTIVE"

    elif action == "suspend":
        if ServerStatus != "ACTIVE":
            return {
                "error": {
                    "message": "Cannot 'suspend' instance {0} while it is in vm_state {1}".format(serverid,ServerStatus),
                    "code": 409
                }
            }

        ServerStatus = "SUSPENDED"

    elif action == "unpause":

        if ServerStatus != "PAUSED":
            return {
                "error": {
                    "message": "Cannot 'suspend' instance {0} while it is in vm_state {1}".format(serverid,
                                                                                                  ServerStatus),
                    "code": 409
                }
            }

        ServerStatus = "ACTIVE"

    elif action == "pause":
        if ServerStatus != "ACTIVE":
            return {
                "error": {
                    "message": "Cannot 'suspend' instance {0} while it is in vm_state {1}".format(serverid,
                                                                                                  ServerStatus),
                    "code": 409
                }
            }

        ServerStatus = "PAUSED"

    elif action == "reboot":
        if ServerStatus == "ERROR":
            return {
                "error": {
                    "message": "Cannot 'reboot' instance {0} while it is in vm_state {1}".format(serverid,
                                                                                                  ServerStatus),
                    "code": 409
                }
            }
        ServerStatus = "ACTIVE"

    else:
        return {"error":{"message":"unspported action","code": 405}}


    return {}











