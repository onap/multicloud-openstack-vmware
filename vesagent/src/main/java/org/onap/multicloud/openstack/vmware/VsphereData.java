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
import java.net.URL;
import java.rmi.RemoteException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;

import org.json.simple.JSONObject;

import com.vmware.vim25.InvalidProperty;
import com.vmware.vim25.ManagedEntityStatus;
import com.vmware.vim25.RuntimeFault;
import com.vmware.vim25.mo.Folder;
import com.vmware.vim25.mo.HostSystem;
import com.vmware.vim25.mo.InventoryNavigator;
import com.vmware.vim25.mo.ManagedEntity;
import com.vmware.vim25.mo.ServiceInstance;
import com.vmware.vim25.mo.VirtualMachine;

public class VsphereData {
	ArrayList<String> hostsArray = new ArrayList<String>();
	VirtualMachine[] vms;

	public static String eventId;
    public String currentDateTime(){
		String sdf = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss").format(Calendar.getInstance().getTime());
		return sdf;
	}
	
	public ServiceInstance getServiceIntanceMeth(VsphereEntity vsphereEntity) throws RemoteException, MalformedURLException{
		System.out.println("getting service instance for connection");
		ServiceInstance si = new ServiceInstance(new URL("https://"+vsphereEntity.getVsphereServerName()+"/sdk"), vsphereEntity.VsphereUsername, vsphereEntity.getVsperePassword(), true);
		System.out.println("connected..");
		return si;
		}
	
	public ManagedEntity getManagedEntityVM(ServiceInstance si,VsphereEntity vsphereEntity) throws RemoteException, MalformedURLException{
		Folder rootFolder = si.getRootFolder();
		ManagedEntity me = new InventoryNavigator(rootFolder).searchManagedEntity("VirtualMachine", vsphereEntity.getVsphereVMname());
		System.out.println("got managed object.. virtual machine...");
		return me;
		
	}
	
	public VsphereDataEntity getAllDataFromVM(ManagedEntity me,VsphereDataEntity data,VsphereEntity vsphereEntity) throws RemoteException, MalformedURLException, Exception{
		
		System.out.println("getting data from vm ..");
		VirtualMachine vm = (VirtualMachine)me;
	    ManagedEntityStatus status = vm.getGuestHeartbeatStatus();
	    System.out.println(currentDateTime()+" Virtual machine: "+vsphereEntity.VsphereVMname+" Status: "+status.toString());
	    Thread.sleep(2000);
	    String heartBeatStatus = status.toString();
	    String sourceName = vm.getName();
	    String sourceType = vm.toString();
	    String sourceType1 = sourceType.substring(0, sourceType.indexOf(":"));
	    String sourceId = vm.getConfig().getUuid();
	    data.setStatus(heartBeatStatus);
	    data.setSourceId(sourceId);
	    data.setSourceName(sourceName);
	    data.setSourceType(sourceType1);
	    System.out.println("saved to VsphereDataEntity");
		return data;
		}
	
	public ManagedEntity[] getManagedEntityHosts(ServiceInstance si,VsphereEntity vsphereEntity) throws InvalidProperty, RuntimeFault, RemoteException{
		Folder rootFolder = si.getRootFolder();
		ManagedEntity[] me = new InventoryNavigator(rootFolder).searchManagedEntities("HostSystem");
		System.out.println("got managed object.. Host systems...");
		return me;
	}
	
	public VirtualMachine[] ListAllVms(ServiceInstance si,VsphereEntity vsphereEntity) throws InvalidProperty, RuntimeFault, RemoteException{
		ManagedEntity[] me = getManagedEntityHosts(si, vsphereEntity);
		for(ManagedEntity hos:me){
	        	HostSystem host = (HostSystem)hos;
	        	hostsArray.add(host.getName());
	        	System.out.println("hosts: "+host.getName());
	        	VirtualMachine[] vms = host.getVms();
	        	System.out.println("No of Vms present in "+host.getName()+"host: "+vms.length);
		}
		return vms;
	}
	@SuppressWarnings("unchecked")
	public void encodeJson(VsphereDataEntity vsphereDataEntity,JSONObject event, JSONObject eventObj,JSONObject commonEventHeader,JSONObject faultFields) throws RemoteException, MalformedURLException, Exception{
		System.out.println("encoding to json.......");
		Double version = 3.0;
		String domain="fault";  
		String eventId  = "ab305d54-85b4-a31b-7db2-fb6b9e546015";
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
		  
		if (vsphereDataEntity.getStatus() !="green") {  
			eventName="Fault_MultiCloud_VMFailure";
			priority="High"; 
			eventSeverity="CRITICAL" ;  //it should be in caps
			alarmCondition="Guest_Os_Failure";
			vfStatus="Active";
			specificProblem="AlarmOn";
			
		} 
		else {
			eventName="Fault_MultiCloud_VMFailureCleared";      
			priority="Normal"; 
			eventSeverity="Normal" ;
			alarmCondition="Vm_Restart";
			vfStatus="Active"; 
			specificProblem="AlarmOff";
		}
		 
		   /* Point to be noted  for start and last epoch time - 
		               for alarm on case both will be the same value 
		               but for alarm off case the lastEpochMicroSec will be current System/Date/Time */
		long unixTime = (System.currentTimeMillis() / 1000L)*1000000 ;
		Long startEpochMicrosec = unixTime;
		Long lastEpochMicrosec = unixTime;
		
		String sourceId =vsphereDataEntity.getSourceId().toString();
		Double faultFieldsVersion=2.0;
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
		List<String> list = new ArrayList<>();
		list.add(Json);
		list.add(alarmCondition);
		return list;
		
	}
	public List<JsonAlarmStorage> listJsonAlarm2(JSONObject json,String alarmCondition, String vesSendStatus){
		System.out.println("adding to list- json and alarm");
		JsonAlarmStorage store = new JsonAlarmStorage();
		List<JsonAlarmStorage> list = new ArrayList<>();
		store.json = json;
		store.alarm=alarmCondition;
		store.vesSendStatus = vesSendStatus;
		list.add(store);
		return list;
		
	}   
}
