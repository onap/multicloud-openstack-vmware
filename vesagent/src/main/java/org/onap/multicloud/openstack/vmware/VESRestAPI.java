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

import java.net.Socket;
import java.util.List;
import java.io.IOException;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.DefaultHttpClient;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
/*Contain all methods for rest api calls*/

@SuppressWarnings("deprecation")
public class VESRestAPI{
    String eventType;
    private StringEntity entity;
    private HttpPost post;
    private Socket sock;
    private DefaultHttpClient client;
    private final Logger log = LoggerFactory.getLogger(VESRestAPI.class);
    private String applicationJson = "application/json";
    private String anyEvent = "any";
    private String batchEvent = "batch";
    private String vesSendStatusSuccess="success";
    @SuppressWarnings({ "resource" })
    public boolean publishAnyEventToVES(VesEntity ves ,JsonStoreMap map, VesTimer timer,String uuidKey,List<JsonAlarmStorage> list, Integer duration,String vesSendStatus) throws IOException{
        try{
            eventType = anyEvent;
            log.info("inside publish any event  method");
            sock = new Socket(ves.getVesip(), ves.getPort());
            log.info(String.valueOf(sock.isConnected()));
            if(sock.isConnected()){
                log.info("list "+list.get(0).json.toString());
                client = new DefaultHttpClient();
                /* check the vesStructure  whether each of the variable like ip address , portnumber , user name and password  contains something or is null */
                if(vesEntitycredentialCheckSuccess(ves)){
                    post = new HttpPost("http://"+ves.getVesip()+":"+ves.getPort()+"/eventListener/v5");
                    log.info(ves.getPort().toString());
                }else{
                    log.info("Null");
                }
                entity = new StringEntity(list.get(0).json.toString());
                post.setEntity(entity);
                post.setHeader("Content-type", applicationJson);
                HttpResponse response = client.execute(post);
                log.info(response.getStatusLine().toString());
                if(vESCollectorSendStatus(response,map,uuidKey,list,timer,vesSendStatus)){
                    return true;
                }
                sock.close();
                client.close();
            }
        }catch(Exception e){
            log.info("VES Collector connection refused, exception occured");
            log.error("error",e);
            list.get(0).vesSendStatus = "failed";
            map.updateMap(uuidKey, list);
            if (!timer.isTimerRunning()){
                timer.startTimer(duration);
            }
            else log.info("VES Collector Connection refused, timer is running ");
           }

        return false;
    }

    @SuppressWarnings("resource")
    public boolean publishBatchEventToVES(VesEntity ves, JSONObject alarmJsonConstructArray,JsonStoreMap map, VesTimer timer,String uuidKey,List<JsonAlarmStorage> list, Integer duration,String vesSendStatus) throws IOException{
        try {
            eventType = batchEvent;
            log.info("inside publish batch event  method");
            sock = new Socket(ves.getVesip(), ves.getPort());
            if(sock.isConnected()){
                log.info("Sending batch");
                client = new DefaultHttpClient();
                if(vesEntitycredentialCheckSuccess(ves))
                {
                     post = new HttpPost("http://"+ves.getVesip()+":"+ves.getPort()+"/eventListener/v5/eventBatch");
                }else{
                    log.info("Null");
                }
                entity = new StringEntity(alarmJsonConstructArray.toJSONString());
                post.setEntity(entity);
                post.setHeader("Content-type", applicationJson);
                post.addHeader("Accept", applicationJson);
                HttpResponse response = client.execute(post);
                log.info(response.getStatusLine().toString());
                if(!connectionRefused(response)){
                    return true;
                }
                if(vESCollectorSendStatus(response,map,uuidKey,list,timer,vesSendStatus)){
                    return true;
                }
            }
            sock.close();
            client.close();
        }catch(Exception e){
            log.info("connection refused, exception occured");
            log.error("error",e);
            list.get(0).vesSendStatus = "failed";
            map.updateMap(uuidKey, list);  //modifying map with vesSendStatus as failed
            log.info("...");
            if (!timer.isTimerRunning()){
                log.info("timer started....");
                timer.startTimer(duration);
            }
            else{
                log.info("Connection refused, timer is running");
            }
        }
        return false;
    }

    public boolean vesEntitycredentialCheckSuccess(VesEntity ves){
        if(ves.getPort()==null || ves.getVesip()==null || ves.getVesPassword()==null || ves.getVesUsername()==null){
            return false;
        }
        return true;
    }


    public boolean vESCollectorSendStatus ( HttpResponse response,JsonStoreMap map,String uuidKey, List<JsonAlarmStorage> list,VesTimer timer,String vesSendStatus) throws ParseException { 
        JsonAlarmStorage store = list.get(0);
        log.info(String.valueOf(list.size()));
        log.info(store.alarm);
        String alarmStatus = store.alarm;
        log.info("inside ves collector method");
        if(response.getStatusLine().getStatusCode()>=200 && response.getStatusLine().getStatusCode()<300){
            log.info("...........");
            if(alarmStatus == "ON" && eventType==anyEvent){
                log.info("alarm on ,event type is any and connection is 200 ok");
                log.info("ves send status"+list.get(0).vesSendStatus);
                log.info("total entries in map: ",map.totalEntriesInMap());
                map.displayALLEntriesInMap();
                list.get(0).vesSendStatus = vesSendStatusSuccess;
                map.updateMap(uuidKey, list);
            }else if(alarmStatus == "ON" && eventType==batchEvent){
                log.info("alarm on ,event type is batch and connection is 200 ok");
                log.info("ves send status"+list.get(0).vesSendStatus);
                log.info("total entries in map:",map.totalEntriesInMap());
                map.displayALLEntriesInMap();
                map.updateMapBatch("success");
            }else if(alarmStatus == "OFF" && (vesSendStatus=="new" ||
                                            vesSendStatus ==vesSendStatusSuccess) && eventType==anyEvent){
                log.info("alarm off and connection ok");
                map.deleteFromMap(uuidKey);
            }else if(alarmStatus == "OFF" && (vesSendStatus=="new" ||
                                            vesSendStatus ==vesSendStatusSuccess) && eventType==batchEvent){
                log.info("alarm off and connection ok");
                map.deleteUsingAlarmCondition(alarmStatus);
            }
            if(timer.isTimerRunning()){
                timer.stopTimer();
            }
            else{
                log.info("timer is not running....");
            }
            return true;
        }else{
            log.info("connection error !200");
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
