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
import java.util.List;
import org.json.simple.JSONObject;
import com.vmware.vim25.mo.ManagedEntity;
import com.vmware.vim25.mo.ServiceInstance;


public class VesAgent {
    static VsphereDataEntity vsphereDataEntity = new VsphereDataEntity();
	static JsonStoreMap map = new JsonStoreMap();
	static List<JsonAlarmStorage> list;
	
	public static void main(String[] args) throws RemoteException, MalformedURLException, Exception {
		
		/* in the VShpere Entity we are storing the VCentre IP Address
		 *  , user name , 
		 *  password , vmname
		 */
		Integer duration = 2000;
		System.out.println("inside main method");
		VsphereEntity vsphereEntity = new VsphereEntity();
		vsphereEntity.setVsphereServerName(args[0]);
		vsphereEntity.setVsphereUsername(args[1]);
		vsphereEntity.setVsperePassword(args[2]);
		vsphereEntity.setVsphereVMname(args[3]);
		
		String alarmCondition = args[4]; // for checking alarm is raised or not
		String vesSendStatus = "default";  //vesSendStatus 
		
		 /* VSphereData contains all method to connect , 
		  * retrieve and 
		  * fetch data using VShpere API
		  */
		
		VsphereData vsphereData  = new VsphereData();
		ServiceInstance si =vsphereData.getServiceIntanceMeth(vsphereEntity);
		
	    /* VesEntity class contains ves collector address
	     * username and password  --> authentication
	     * port
	     */
		
		VesEntity vesEntity = new VesEntity();
		vesEntity.setVesip("10.110.208.210");
		vesEntity.setVesUsername("");
		vesEntity.setVesPassword("");
		vesEntity.setPort(8080);
		
		/*VESRestAPI class having all rest api call methods
		 * like publishAnyEvent,
		 *  publishBatchEvent
		 */
		VESRestAPI vesRestAPI= new VESRestAPI();
		
		
		JSONObject eventObj = new JSONObject();
		JSONObject event = new JSONObject();
		JSONObject commonEventHeader = new JSONObject();
		JSONObject faultFields = new JSONObject();
		
		VesTimer timer = new VesTimer(vesEntity, map, vesRestAPI);
		
		
		
		
		while(true){
			ManagedEntity me = vsphereData.getManagedEntityVM(si,vsphereEntity);
			VsphereDataEntity entity = vsphereData.getAllDataFromVM(me,vsphereDataEntity,vsphereEntity);
			
			String heartBeatStatus = vsphereDataEntity.getStatus();
			System.out.println(heartBeatStatus);
			String uuid_key = vsphereDataEntity.getSourceId();
			
		    if(heartBeatStatus!="green"){
		    	//encode json
		    	if(map.isJsonFound(uuid_key) && map.retrieveAlarmConditionFromMap(uuid_key) == "ON"){
		    		System.out.println("alarm ON already raised");
		    	}
		    	else if(!map.isJsonFound(uuid_key)){
		    		alarmCondition = "ON";
		    		vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields);
		    		list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
		    		//JSONObject alarmJsonConstruct = vsphereData.encodeJson(entity);
		    		System.out.println(list.get(0).json+" :"+list.get(0).alarm+" :"+list.get(0).vesSendStatus);
		    		
		    		//String json = event.toJSONString();
		    		//System.out.println(json);
		    		
		    		//map.addToMap(json, key);
		    		//vesRestAPI.publishAnyEventToVES(vesEntity, event,null,map, timer);
		    		vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key, list,duration);
		    		System.out.println("published ");
		    	}
		    	
		    }
		    else if(heartBeatStatus == "green"){
		    	if(map.isJsonFound(uuid_key) &&  map.retrieveAlarmConditionFromMap(uuid_key) == "ON"){
		    		alarmCondition = "OFF";
		    		vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields);
		    		list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
		    		
		    		String json = event.toJSONString();
		    		System.out.println(json);
		    		vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key,list,duration);
				
				
					
					 //we have to check whether the publishAnyEventToVES is successful based on the return value 
				/*if(vesRestAPI.publishAnyEventToVES(vesEntity, event)==true){
					System.out.println("delete from map");
					map.deleteFromMap(key);
				}*/
				
				}
		    
		    }
		    Thread.sleep(2000);
		}    
	}

	
}

			

				
		
			
			
			
			
	
		

	


