 /* Copyright (c) 2017 VMware, Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at:
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 */

package org.onap.multicloud.openstack.vmware;

import java.net.MalformedURLException;
import java.rmi.RemoteException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

import org.json.simple.JSONObject;

public class VsphereData {

    public VsphereDataEntity  gettingVMInfo(JSONObject js,VsphereDataEntity vsphereDataEntity,VsphereEntity vsphereEntity){
        String vsphereVMname = (String) js.get("Name");
        vsphereEntity.setVsphereVMname(vsphereVMname);
        vsphereDataEntity.setSourceName(vsphereVMname);
        String status = (String) js.get("Heartbeatstatus");
        vsphereDataEntity.setStatus(status.toString());

        String instance_uuid=(String) js.get("Instance UUID");
        vsphereDataEntity.setSourceId(instance_uuid);

        String sourceType="VirtualMachine";
        vsphereDataEntity.setSourceType(sourceType);

        System.out.println(vsphereDataEntity.getSourceName());
        System.out.println(vsphereDataEntity.getSourceId());

        System.out.println(vsphereDataEntity.getStatus());
            System.out.println(vsphereDataEntity.getSourceType());

        return vsphereDataEntity;
    }


    @SuppressWarnings("unchecked")
    public void encodeJson(VsphereDataEntity vsphereDataEntity,JSONObject event, JSONObject eventObj,JSONObject commonEventHeader,JSONObject faultFields, JsonStoreMap map) throws RemoteException, MalformedURLException, Exception{
        System.out.println("encoding to json.......");
        Double version = 3.0;
        String domain="fault";

        UUID uuid = UUID.randomUUID();


        //String eventId  = "ab305d54-85b4-a31b-7db2-fb6b9e546015";
        String sourceName=vsphereDataEntity.getSourceName();
        String reportingEntityName = "Multi-Cloud";
        Integer sequence=0;
        //String eventType="GuestOS";
        String eventName="";
        String priority="";
        String eventSeverity="";
        String alarmCondition="";
        String vfStatus="";
        String specificProblem="";
        long unixTime = (System.currentTimeMillis() / 1000L)*1000000 ;
        Long startEpochMicrosec = null;
        Long lastEpochMicrosec = null;
        String eventId="";
        String sourceId =vsphereDataEntity.getSourceId().toString();
        Double faultFieldsVersion=2.0;
        if (vsphereDataEntity.getStatus() !="green") {
            eventName="Fault_MultiCloud_VMFailure";
            priority="High";
            eventSeverity="CRITICAL" ;  //it should be in caps
            alarmCondition="Guest_Os_Failure";
            vfStatus="Active";
            specificProblem="AlarmOn";
            startEpochMicrosec = unixTime;
            lastEpochMicrosec = unixTime;
            eventId = uuid.toString();
        }
        else {
            eventName="Fault_MultiCloud_VMFailureCleared";
            priority="Normal";
            eventSeverity="Normal" ;
            alarmCondition="Vm_Restart";
            vfStatus="Active";
            specificProblem="AlarmOff";

            JSONObject json = map.retrieveJsonFromMap(sourceId);
            JSONObject e1 = (JSONObject) json.get("event");
            JSONObject c1 =(JSONObject) e1.get("commonEventHeader");
            String eventIdRetrieved = (String) c1.get("eventId");
            Long startEpochMicrosecRetrieved = (Long) c1.get("startEpochMicrosec");

            startEpochMicrosec = startEpochMicrosecRetrieved;
            lastEpochMicrosec = unixTime;
            eventId=eventIdRetrieved;
        }
           /* Point to be noted  for start and last epoch time -
            for alarm on case both will be the same value
            but for alarm off case the lastEpochMicroSec will be current System/Date/Time */

        /*String eventSourceType="Virtual Machine";
        String  eventCategory="Availability";
        String alarmAdditionalInformation=" ";*/

        //here we have to create jsonobjects
        //JSONObject commonEventHeader = new JSONObject();
        commonEventHeader.put("version", version);
        commonEventHeader.put("domain",domain);
        commonEventHeader.put("eventName",eventName);
        //commonEventHeader.put("eventType",eventType);
        commonEventHeader.put("eventId",eventId);
        commonEventHeader.put("sequence",sequence);
        commonEventHeader.put("priority",priority);
        commonEventHeader.put("reportingEntityName",reportingEntityName);
        commonEventHeader.put("sourceId",sourceId);
        commonEventHeader.put("sourceName",sourceName);
        commonEventHeader.put("startEpochMicrosec",startEpochMicrosec);
        commonEventHeader.put("lastEpochMicrosec",lastEpochMicrosec);

        //JSONObject faultFields = new JSONObject();
        faultFields.put("faultFieldsVersion",faultFieldsVersion );
        faultFields.put("eventSeverity",eventSeverity );
        faultFields.put("alarmCondition",alarmCondition );
        faultFields.put("specificProblem",specificProblem );
        faultFields.put("vfStatus",vfStatus );
        faultFields.put("alarmInterfaceA", "aaaa");
        faultFields.put("eventSourceType", "other");

        //JSONObject eventObj = new JSONObject();
        eventObj.put("commonEventHeader", commonEventHeader);
        eventObj.put("faultFields",faultFields);

        //JSONObject event = new JSONObject();
        event.put("event", eventObj);
    }

    public void encodeJsonBatch(JsonStoreMap map){

    }

    public List<String> listJsonAlarm(String Json,String alarmCondition){
        System.out.println("adding to list- json and alarm");
        List<String> list = new ArrayList<String>();
        list.add(Json);
        list.add(alarmCondition);
        return list;
    }

    public List<JsonAlarmStorage> listJsonAlarm2(JSONObject json,String alarmCondition, String vesSendStatus){
        System.out.println("adding to list- json and alarm");
        JsonAlarmStorage store = new JsonAlarmStorage();
        List<JsonAlarmStorage> list = new ArrayList<JsonAlarmStorage>();
        store.json = json;
        store.alarm=alarmCondition;
        store.vesSendStatus = vesSendStatus;
        list.add(store);
        return list;
    }
}
