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

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.json.simple.JSONObject;

public class VsphereData {
    private final Logger log = LoggerFactory.getLogger(VsphereData.class);
    public VsphereDataEntity  gettingVMInfo(JSONObject js,VsphereDataEntity vsphereDataEntity,VsphereEntity vsphereEntity){
        String vsphereVMname = (String) js.get("Name");
        vsphereEntity.setVsphereVMname(vsphereVMname);
        vsphereDataEntity.setSourceName(vsphereVMname);
        String status = (String) js.get("Heartbeatstatus");
        vsphereDataEntity.setStatus(status);

        String instanceUuid=(String) js.get("Instance UUID");
        vsphereDataEntity.setSourceId(instanceUuid);

        String sourceType="VirtualMachine";
        vsphereDataEntity.setSourceType(sourceType);

        log.info(vsphereDataEntity.getSourceName());
        log.info(vsphereDataEntity.getSourceId());

        log.info(vsphereDataEntity.getStatus());
        log.info(vsphereDataEntity.getSourceType());

        return vsphereDataEntity;
    }


    @SuppressWarnings("unchecked")
    public void encodeJson(VsphereDataEntity vsphereDataEntity,JSONObject event, JSONObject eventObj,JSONObject commonEventHeader,JSONObject faultFields, JsonStoreMap map) {
        log.info("encoding to json.......");
        Double version = 3.0;
        String domain="fault";

        UUID uuid = UUID.randomUUID();

        String sourceName=vsphereDataEntity.getSourceName();
        String reportingEntityName = "Multi-Cloud";
        Integer sequence=0;
        String eventName;
        String priority;
        String eventSeverity;
        String alarmCondition;
        String vfStatus;
        String specificProblem;
        long unixTime = (System.currentTimeMillis() / 1000L)*1000000 ;
        Long startEpochMicrosec;
        Long lastEpochMicrosec;
        String eventId;
        String sourceId =vsphereDataEntity.getSourceId();
        Double faultFieldsVersion=2.0;
        if (!vsphereDataEntity.getStatus().equals("green")) {
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
            eventSeverity="NORMAL" ;
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

        //here we have to create jsonobjects
        commonEventHeader.put("version", version);
        commonEventHeader.put("domain",domain);
        commonEventHeader.put("eventName",eventName);
        commonEventHeader.put("eventId",eventId);
        commonEventHeader.put("sequence",sequence);
        commonEventHeader.put("priority",priority);
        commonEventHeader.put("reportingEntityName",reportingEntityName);
        commonEventHeader.put("sourceId",sourceId);
        commonEventHeader.put("sourceName",sourceName);
        commonEventHeader.put("startEpochMicrosec",startEpochMicrosec);
        commonEventHeader.put("lastEpochMicrosec",lastEpochMicrosec);

        faultFields.put("faultFieldsVersion",faultFieldsVersion );
        faultFields.put("eventSeverity",eventSeverity );
        faultFields.put("alarmCondition",alarmCondition );
        faultFields.put("specificProblem",specificProblem );
        faultFields.put("vfStatus",vfStatus );
        faultFields.put("alarmInterfaceA", "aaaa");
        faultFields.put("eventSourceType", "other");

        eventObj.put("commonEventHeader", commonEventHeader);
        eventObj.put("faultFields",faultFields);

        event.put("event", eventObj);
    }


    public List<JsonAlarmStorage> listJsonAlarm(JSONObject json,String alarmCondition, String vesSendStatus){
        log.info("adding to list- json and alarm");
        JsonAlarmStorage store = new JsonAlarmStorage();
        List<JsonAlarmStorage> list = new ArrayList<>();
        store.json = json;
        store.alarm=alarmCondition;
        store.vesSendStatus = vesSendStatus;
        list.add(store);
        return list;
    }
}
