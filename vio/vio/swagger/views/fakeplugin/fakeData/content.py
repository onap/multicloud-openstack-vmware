
from vio.pub.config.config import MSB_SERVICE_PORT
from vio.pub.config.config import MSB_SERVICE_IP

from collections import defaultdict
from uuid import uuid4
from datetime import datetime
from datetime import timedelta

MSB_SERVER = MSB_SERVICE_IP+":"+MSB_SERVICE_PORT

Token = "gAAAAABZmlkS3H24i7446u41QoDMMEFi49sUbYiB2fqrZq00TR92RDLxt4AWzHsBa36IeWeY_eVEnDWAjIuV" \
         "vK2osp6mPTEKGCvywrksCorunJqPCf46nBhGt-P4bqXMUWRMgowfIS2_kv1pQwvoP00_Rs6KlDaWt-miEu7s24m3En9Qsbg8Ecw"


TenatId = "c049d4ad1dee475db8c3627bef9e916a"




serverMapps = defaultdict(dict)



def keystoneVersion():
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
                    "href": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/vmware_fake/identity/v3",
                    "rel": "self"
                }
            ]
        }

    }

    data['version']['update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    return data



def keystoneToken(teanatid=None):

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
                {  "url": "http://"+MSB_SERVER+"/api/multicloud-vio/v0/vmware_fake/cinder/"+TenatId,
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
                    "url": "http://"+MSB_SERVER+"/api/multicloud-vio/v0/vmware_fake/neutron/"+TenatId,
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
                    "url": "http://"+MSB_SERVER+"/api/multicloud-vio/v0/vmware_fake/identity",
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
                        "url": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/vmware_fake/heat/"+TenatId,
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
                        "url": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/vmware_fake/nova/"+TenatId,
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
                        "url": "http://" + MSB_SERVER + "/api/multicloud-vio/v0/vmware_fake/glance",
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
                            "self": "http://127.0.0.1:5000/v3/projects/0cf31a5c8da74fe3afb14683f9043f7b"
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
                            "self": "http://127.0.0.1:5000/v3/projects/3888e02273224c7a93c961d8dde8094f"
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
                            "self": "http://127.0.0.1:5000/v3/projects/e75f80048997438dbc0bfaa822dfdf65"
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


def showProject(token,projectid=""):
    if token != Token:
        return {"error": {"message": "unauthorization", "code": 401}}


    data = {
            "project":
                {
                    "is_domain": "false", "description": "Admin Project", "links":
                    {
                        "self": "https://127.0.0.1:5000/v3/projects/9e8a26d207ef454981750e98e42e9aa8"
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
                    "host_ip": "127.0.0.1",
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

   
    data ={"servers":[]}
    for k,v in serverMapps.iteritems():
        server = {"id":k,
                "links":[
                    {
                        "href": "https://127.0.0.1:8774/v2.1/" + v['tenantid']+"/servers/" + k,
                        "ref": "self"
                    },
                    {
                        "href": "https://127.0.0.1:8774/v2.1/" + v['tenantid'] + "/servers/" + k,
                        "ref": "bookmark"
                    }
                    
                ],
                "naem":v['name']
        
                }
        data['servers'].append(server)
        
    return data


def showServerDetail(token,serverid,tenantid=None):
    if token != Token:
        return {"error":{"message":"unauthorization","code":401}}

    if serverid  not in  serverMapps:
        return {"error": {"message":"instance {0} is not exsit".format(serverid),"code":404}}

    try:
        _serverStatus(serverid)
    except ValueError:
        return {"error": {"message": "instance {0} is not exsit".format(serverid), "code": 404}}


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
                    "href": "https://127.0.0.1:8774/v2.1/"+TenatId+"/servers/" + serverid,
                    "rel": "self"
                },
                {
                    "href": "https://127.0.0.1:8774/"+TenatId+"/servers/" + serverid,
                    "rel": "bookmark"
                }
            ],
            "image": {
                "id": "0c80630a-eb3a-47c0-950a-facb2721139c",
                "links": [
                    {
                        "href": "https://127.0.0.1:8774/"+TenatId+"/images/0c80630a-eb3a-47c0-950a-facb2721139c",
                        "rel": "bookmark"
                    }
                ]
            },

            "OS-EXT-STS:vm_state": serverMapps[serverid]['status'].lower(),
            "OS-EXT-SRV-ATTR:instance_name": "instance-00000053",
            "OS-SRV-USG:launched_at": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            "flavor": {
                "id": "13",
                "links": [
                    {
                        "href": "https://127.0.0.1:8774/"+TenatId+"/flavors/13",
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
            "updated": (datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
            "hostId": "5a9fc696507589459e64ba6dfb0ad1570c0952cdd1c184b0b7bdde9a",
            "OS-EXT-SRV-ATTR:host": "compute01",
            "OS-SRV-USG:terminated_at": "null",
            "key_name": "onap_key_L6dr",
            "OS-EXT-SRV-ATTR:hypervisor_hostname": "domain-c202.22bfc05c-da55-4ba6-ba93-08d9a067138e",
            "name": "vio-mso",
            "created": serverMapps[serverid]['createTime'],
            "tenant_id": tenantid,
            "os-extended-volumes:volumes_attached": [],
            "config_drive": ""
        }
    }

    return data



def deleteServer(token,serverid):
    if token != Token:
        return {"error": {"message":"unauthorization","code":401}}

    if serverid not in  serverMapps:
        return {"error": {"message": "instance {0} is not exsit".format(serverid), "code": 404}}

    serverMapps[serverid]['turnStatusTime'] = datetime.now()
    serverMapps[serverid]['status'] = "DELETING"

    #del serverMapps[serverid]
    
    return {}


def operator_server(token,serverid,action):
    if token != Token:
        return {"error": {"message":"unauthorization","code":401}}

    if serverid not in serverMapps:
        return {"error": {"message":"instance {0} is not exsit".format(serverid),"code":404}}
    try:
        _serverStatus(serverid)
    except ValueError:
        return  {"error": {"message": "instance {0} is not exsit".format(serverid), "code": 404}}


    if action == "os-stop":
        if serverMapps[serverid]['status'] != "ACTIVE":
            return {
                "error": {
                "message": "Cannot 'stop' instance {0} while it is in vm_state {1}".format(serverid,serverMapps[serverid]['status']),
                "code": 409
                }
            }

        serverMapps[serverid]['turnStatusTime'] = datetime.now()
        serverMapps[serverid]['status'] = "POWERING_OFF"

        
    elif action == "os-start":
        if serverMapps[serverid]['status'] != "SHUTDOWN":
            return {
                "error": {
                    "message": "Cannot 'start' instance {0} while it is in vm_state {1}".format(serverid,serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['turnStatusTime'] = datetime.now()
        serverMapps[serverid]['status'] = "POWERING_ON"
        #serverMapps[serverid]['status'] = "ACTIVE"


    elif action == "resume":
        if serverMapps[serverid]['status'] != "SUSPENDED":
            return {
                "error": {
                    "message": "Cannot 'resume' instance {0} while it is in vm_state {1}".format(serverid,serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "ACTIVE"

    elif action == "suspend":
        if serverMapps[serverid]['status'] != "ACTIVE":
            return {
                "error": {
                    "message": "Cannot 'suspend' instance {0} while it is in vm_state {1}".format(serverid,serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "SUSPENDED"

    elif action == "unpause":

        if serverMapps[serverid]['status'] != "PAUSED":
            return {
                "error": {
                    "message": "Cannot 'unpause' instance {0} while it is in vm_state {1}".format(serverid,
                                                                                                  serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "ACTIVE"

    elif action == "pause":
        if serverMapps[serverid]['status'] != "ACTIVE":
            return {
                "error": {
                    "message": "Cannot 'pause' instance {0} while it is in vm_state {1}".format(serverid,
                                                                                                  serverMapps[serverid]['status']),
                    "code": 409
                }
            }

        serverMapps[serverid]['status'] = "PAUSED"

    elif action == "reboot":
        if serverMapps[serverid]['status'] == "ERROR" or serverMapps[serverid]['status'] == "REBOOTING":
            return {
                "error": {
                    "message": "Cannot 'reboot' instance {0} while it is in vm_state {1}".format(serverid,
                                                                                                  serverMapps[serverid]['status']),
                    "code": 409
                }
            }
        serverMapps[serverid]['turnStatusTime'] = datetime.now()
        serverMapps[serverid]['status'] = "REBOOTING"

        #serverMapps[serverid]['status'] = "ACTIVE"

    else:
        return {"error":{"message":"unspported action","code": 405}}


    return {}



def createInstance(token,minCount=1,maxCount=2,json=None):

    if token != Token:
        return {"error": {"message":"unauthorization","code":401}}

    try:
           name = json['server']['name']

    except Exception as e:
        return  {"error": {"message": "invalidate data", "code":403}}


    uid = str(uuid4())
    data = {
                "server": {
                    "id": uid,
                    "links": [
                        {
                            "href": "http://openstack.example.com/v2/"+TenatId+"/servers/"+uid,
                            "rel": "self"
                        },
                        {
                            "href": "http://openstack.example.com/"+TenatId+"/servers/"+uid,
                            "rel": "bookmark"
                        }
                    ],
                    "name": name
                }
            }

    serverMapps[uid] = {"name":name,"tenantid":TenatId,"status":"BUILDING",'createTime':(datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
                        "turnStatusTime":datetime.now()}
    
    return data






def _serverStatus(serverid):

        startTime = serverMapps[serverid]['turnStatusTime']
        currentTime = datetime.now()
        print currentTime - startTime
        if currentTime - startTime >= timedelta(seconds=10):
            if serverMapps[serverid]['status'] == "SPAWNING" or serverMapps[serverid]['status'] == "BUILDING":
                serverMapps[serverid]['status'] = "ACTIVE"
            elif serverMapps[serverid]['status'] == "DELETING":
                del serverMapps[serverid]
                raise ValueError()

            elif serverMapps[serverid]['status'] == "POWERING_OFF":
                serverMapps[serverid]['status'] = "SHUTDOWN"
            elif serverMapps[serverid]['status'] == "POWERING_ON":
                serverMapps[serverid]['status'] = "ACTIVE"

            elif serverMapps[serverid]['status'] == "REBOOTING":
                serverMapps[serverid]['status'] = "ACTIVE"
            else:
                pass
        elif timedelta(seconds=5) <= currentTime - startTime < timedelta(seconds=10):
            if serverMapps[serverid]['status'] == "BUILDING":
                serverMapps[serverid]['status'] = "SPAWNING"
        else:
            pass





