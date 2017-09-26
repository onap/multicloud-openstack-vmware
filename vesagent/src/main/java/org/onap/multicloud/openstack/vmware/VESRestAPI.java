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

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.List;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

/*Contain all methods for rest api calls*/

@SuppressWarnings("deprecation")
public class VESRestAPI{
	int counter_connectionRefused = 0;
	VesEntity ves = null;
	public StringEntity entity;
	
	 
	@SuppressWarnings({ "resource" })
	public boolean publishAnyEventToVES(VesEntity ves ,JsonStoreMap map, VesTimer timer,String uuid_key,List<JsonAlarmStorage> list, Integer duration) throws ClientProtocolException, IOException, ParseException{
		try{
			System.out.println("inside publish any event  method");
			Socket sock = new Socket(ves.getVesip(), ves.getPort());
			System.out.println(sock.isConnected());
			if(sock.isConnected()){
				System.out.println("list "+list.get(0).json);
				DefaultHttpClient client = new DefaultHttpClient(); 
				/* check the vesStructure  whether each of the variable like ip address , portnumber , user name and password  contains something or is null */
				HttpPost post = new HttpPost("http://"+ves.getVesip()+":"+ves.getPort()+"/eventListener/v5");
				System.out.println(ves.getPort());
				entity = new StringEntity(list.get(0).json.toString());
				post.setEntity(entity);
				post.setHeader("Content-type", "application/json");
				HttpResponse response = client.execute(post);
				System.out.println(response.getStatusLine());
				BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
				System.out.println(response.getEntity().getContent().toString());
				StringBuffer result = new StringBuffer();
				String line = "";
				while ((line = rd.readLine()) != null) {
					result.append(line);
				}
				System.out.println(result);
				if(VESCollectorSendStatus(response,map,uuid_key,list,duration)){
					return true;
				}
			}
		}catch(Exception e){
			System.out.println("connection refused exception error occured");
			if (counter_connectionRefused==0) {
				System.out.println("counter_connectionRefused==0");
				list.get(0).vesSendStatus = "pending";
				map.addToMap(uuid_key, list);
				if (!timer.isTimerRunning()){
					timer.startTimer(duration);
				}
				else System.out.println("counter = 0 and timer is running");
			}
			else if(counter_connectionRefused > 0){
				System.out.println("counter_connectionRefused==0");
				if(timer.isTimerRunning()){
					list.get(0).vesSendStatus = "pending";
					map.addToMap("key", list);
				}
				else if(timer.isTimerRunning()){
					list.get(0).vesSendStatus = "pending";
					map.addToMap("key", list);
					//timer.startTimer(duration);
				}
			}
		}
		return false;
	}

			
	
	
	@SuppressWarnings("resource")
	public boolean publishBatchEventToVES(VesEntity ves, JSONObject alarmJsonConstructArray) throws FileNotFoundException, IOException, ParseException{
		System.out.println("Sending batch");
		DefaultHttpClient client = new DefaultHttpClient(); 
		HttpPost post = new HttpPost("http://"+ves.getVesip()+":"+ves.getPort()+"/eventListener/v5/eventBatch");
		entity = new StringEntity(alarmJsonConstructArray.toJSONString());
		post.setEntity(entity);
		post.setHeader("Content-type", "application/json");
		post.addHeader("Accept", "application/json");
		HttpResponse response = client.execute(post);
		System.out.println(response.getStatusLine());
		BufferedReader rd = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
		System.out.println(response.getEntity().getContent().toString());
		StringBuffer result = new StringBuffer();
		String line = "";
		while ((line = rd.readLine()) != null) {
			result.append(line);
		}
		System.out.println(result);
		if(!connectionRefused(response))
			return true;
		return false;   
   }
	

	public boolean VESCollectorSendStatus ( HttpResponse response,JsonStoreMap map,String uuid_key, List<JsonAlarmStorage> list, Integer duration) throws ParseException { 
		Integer code = response.getStatusLine().getStatusCode();
		JsonAlarmStorage store = list.get(0);
		System.out.println(list.size());
		System.out.println(store.alarm);
		String alarmStatus = store.alarm;
		System.out.println("insiide ves collector method");
		if(code>=200 && code<300){
			System.out.println();;
			if(alarmStatus == "ON"){
				System.out.println("alarm on and connection is 200 ok");
				list.get(0).vesSendStatus ="hi...";
				System.out.println("Test list for satus"+list.get(0).vesSendStatus);
				map.addToMap(uuid_key, list);
				//map.addToMap("sample key", list);
				
				System.out.println(map.totalEntriesInMap());
				//System.out.println(map.retrieveALLFromMapBatch());
				map.retrieveALLFromMap();
				
				
			}
			else if(alarmStatus == "OFF"){
				System.out.println("alarm off and connection ok");
				map.deleteFromMap("key");
			}
			
		return true;
		}
		else{
			
			
			System.out.println("connection error !200");
		return false;
		}
	}
		
			

	public boolean connectionRefused(HttpResponse response){
		if(response.getStatusLine().getStatusCode()!=200){
			return true;
		}
		return false;
		
	}


}



