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
   static String eventType;
    int counter_connectionRefused = 0;
    VesEntity ves = null;
    public StringEntity entity;
    static HttpPost post = null;

    @SuppressWarnings({ "resource" })
    public boolean publishAnyEventToVES(VesEntity ves ,JsonStoreMap map, VesTimer timer,String uuid_key,List<JsonAlarmStorage> list, Integer duration,String vesSendStatus) throws ClientProtocolException, IOException, ParseException{
        try{
           eventType = "any";
            System.out.println("inside publish any event  method");
            Socket sock = new Socket(ves.getVesip(), ves.getPort());
            System.out.println(sock.isConnected());
            if(sock.isConnected()){
                System.out.println("list "+list.get(0).json);
                DefaultHttpClient client = new DefaultHttpClient();
                /* check the vesStructure  whether each of the variable like ip address , portnumber , user name and password  contains something or is null */
                if(vesEntitycredentialCheckSuccess(ves)==true){
                    post = new HttpPost("http://"+ves.getVesip()+":"+ves.getPort()+"/eventListener/v5");
                    System.out.println(ves.getPort());
                }else{
                    System.out.println("Null");
                }

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
                if(VESCollectorSendStatus(response,map,uuid_key,list,timer,duration,vesSendStatus)){
                    return true;
                }
            }
        }catch(Exception e){
            System.out.println("VES Collector connection refused exception error occured");
            list.get(0).vesSendStatus = "failed";
            map.UpdateMap(uuid_key, list);
            if (!timer.isTimerRunning()){
                timer.startTimer(duration);
            }
            else
            {
                System.out.println("VES Collector Connection Refushed Timer is running ");
            }
        }
        return false;
    }

    @SuppressWarnings("resource")

    public boolean publishBatchEventToVES(VesEntity ves, JSONObject alarmJsonConstructArray,JsonStoreMap map, VesTimer timer,String uuid_key,List<JsonAlarmStorage> list, Integer duration) throws FileNotFoundException, IOException, ParseException{
        try {
            eventType = "batch";
            System.out.println("inside publish batch event  method");
            Socket sock = new Socket(ves.getVesip(), ves.getPort());
            System.out.println(sock.isConnected());
            if(sock.isConnected())
            {
                System.out.println("Sending batch");
                DefaultHttpClient client = new DefaultHttpClient();
                if(vesEntitycredentialCheckSuccess(ves)==true)
                {
                    HttpPost post = new HttpPost("http://"+ves.getVesip()+":"+ves.getPort()+"/eventListener/v5/eventBatch");
                }else{
                    System.out.println("Null");
                }
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
                if(!connectionRefused(response)){
                    return true;
                }
            }
     /*if(VESCollectorSendStatus(response,map,uuid_key,list,timer,duration,vesSendStatus)){
    return true;
    } */
        }
        catch(Exception e){
            System.out.println("connection refused exception error occured");
            list.get(0).vesSendStatus = "failed";
            map.UpdateMap(uuid_key, list);  //modifying map with vesSendStatus as failed
            System.out.println("...");
            if (!timer.isTimerRunning()){
                System.out.println("timer started....");
                timer.startTimer(duration);
            }
            else{
                System.out.println("Connection refused timer is running");
            }
    }
    return false;
}

    public boolean vesEntitycredentialCheckSuccess(VesEntity ves){
        if(ves.getPort()==null | ves.getVesip()==null|ves.getVesPassword()==null|ves.getVesUsername()==null){
            return false;
        }
        return true;
    }

    public boolean VESCollectorSendStatus ( HttpResponse response,JsonStoreMap map,String uuid_key, List<JsonAlarmStorage> list,VesTimer timer, Integer duration,String vesSendStatus) throws ParseException { 
    Integer code = response.getStatusLine().getStatusCode();
    JsonAlarmStorage store = list.get(0);
    System.out.println(list.size());
    System.out.println(store.alarm);
    String alarmStatus = store.alarm;
    System.out.println("insiide ves collector method");
    if(code>=200 && code<300){
        System.out.println();
        if(alarmStatus == "ON"){
            System.out.println("alarm on and connection is 200 ok");
            //map.addToMap("sample key", list);
            System.out.println("Test list for satus"+list.get(0).vesSendStatus);
            System.out.println(map.totalEntriesInMap());
            map.retrieveALLFromMap();
            if(eventType=="any"){
                list.get(0).vesSendStatus = "success";
                map.UpdateMap(uuid_key, list);
            }
            else if(eventType=="batch"){
                map.UpdateMapBatch("success");
            }
        }
        else if(alarmStatus == "OFF" && (vesSendStatus=="new" || vesSendStatus =="success"))
        {
            System.out.println("alarm off and connection ok");
            if(eventType=="any"){
                map.deleteFromMap(uuid_key);
            }else if(eventType=="batch"){
                map.deleteUsingAlarmCondition(alarmStatus);
            }
        }
        if(timer.isTimerRunning()){
            timer.stopTimer();
        }
        else{
            System.out.println("timer is not running....");
        }
    return true;
    }
    else
    {
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
