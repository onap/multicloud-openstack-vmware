#!/usr/bin/env python
# VMware vSphere Python SDK
# Copyright (c) 2008-2015 VMware, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
List the vms on an ESX / vCenter host
"""

from __future__ import print_function
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import argparse
import atexit
import getpass
import ssl
import json

fp = None
JsonFile = None
listjson = []

AgntProps = {}
with open("/opt/etc/Agent.properties") as propfile:
  for line in propfile:
    name, var = line.partition("=")[::2]
    AgntProps[name.strip()] = var
JsonFile = AgntProps["Python_Output_Json"].strip()

def GetArgs():
   """
   Supports the command-line arguments listed below.
   """
   parser = argparse.ArgumentParser(
       description='Process args for retrieving all the Virtual Machines')
   parser.add_argument('-s', '--host', required=True, action='store',
                       help='Remote host to connect to')
   parser.add_argument('-o', '--port', type=int, default=443, action='store',
                       help='Port to connect on')
   parser.add_argument('-u', '--user', required=True, action='store',
                       help='User name to use when connecting to host')
   parser.add_argument('-p', '--password', required=True, action='store',
                       help='Password to use when connecting to host')
   args = parser.parse_args()
   return args


def PrintVmInfo(vm, depth=1):

   """
   Print information for a particular virtual machine or recurse into a folder
   or vApp with depth protection
   """
   maxdepth = 10


   # if this is a group it will have children. if it does, recurse into them
   # and then return
   if hasattr(vm, 'childEntity'):
      if depth > maxdepth:
         return
      vmList = vm.childEntity
      for c in vmList:
         PrintVmInfo(c, depth+1)
      return


   # if this is a vApp, it likely contains child VMs
   # (vApps can nest vApps, but it is hardly a common usecase, so ignore that)
   if isinstance(vm, vim.VirtualApp):
      vmList = vm.vm
      for c in vmList:
         PrintVmInfo(c, depth + 1)
      return


   summary = vm.summary
   #print("Name       : ", summary.config.name)
   #print("Path       : ", summary.config.vmPathName)
   #print("Guest      : ", summary.config.guestFullName)
   #print("Instance UUID: ", summary.config.instanceUuid)
   #print("Heartbeatstatus: ", vm.guestHeartbeatStatus)
   if summary.config.name and vm.guestHeartbeatStatus:
     singleinfo={}
     singleinfo.update({"Name":summary.config.name})
     singleinfo.update({"Instance UUID":summary.config.instanceUuid})
     singleinfo.update({"Heartbeatstatus":vm.guestHeartbeatStatus})
     #print ("Final SINGLEINFO")
     listjson.append(singleinfo)
   else:
    print ("NAME, UUID OR HEARTBEAT NOT PRESENT")


def GetContent(args, context):
   if hasattr(ssl, '_create_unverified_context'):
      context = ssl._create_unverified_context()
   si = SmartConnect(host=args.host,
                     user=args.user,
                     pwd=args.password,
                     port=int(args.port),
                     sslContext=context)
   if not si:
       print("Could not connect to the specified host using specified "
             "username and password")
       return -1

   atexit.register(Disconnect, si)
   return si.RetrieveContent()


def CreateJsonList(content):
   for child in content.rootFolder.childEntity:
      if hasattr(child, 'vmFolder'):
         datacenter = child
         vmFolder = datacenter.vmFolder
         vmList = vmFolder.childEntity
         for vm in vmList:
           PrintVmInfo(vm)
   print (listjson)
   return listjson


def CreateJsonFile(jsonrecord):
   if(len(jsonrecord) == 0):
     return False
   else:
     #Return False if File Location is None
     if not JsonFile:
       return False
     else:
       print("Json File Location is:",JsonFile)
       fp = open(JsonFile, 'w')
       json.dump(jsonrecord, fp,sort_keys=True, indent=2)
       fp.close()
       return True


def main():
   """
   Simple command-line program for listing the virtual machines on a system.
   """
   args = GetArgs()
   context = None
   content = GetContent(args, context)
   jsonrecord = CreateJsonList(content)
   if(True == CreateJsonFile(jsonrecord)):
     return 0
   else:
     return -1

# Start program
if __name__ == "__main__":
   main()
