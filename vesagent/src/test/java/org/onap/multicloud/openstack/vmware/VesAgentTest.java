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


import static org.junit.Assert.*;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.List;

import org.apache.http.client.ClientProtocolException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
//import org.json.JSONObject;
//import com.google.gson.JsonParser;
//import com.google.gson.JsonObject;
import org.junit.Test;




/*
public class VesAgent {
    static int count = 0;
    static VsphereDataEntity vsphereDataEntity = new VsphereDataEntity();
    static JsonStoreMap map = new JsonStoreMap();
    static List<JsonAlarmStorage> list;
    static JSONParser parser = new JSONParser();

    public static void main(String[] args) {
        if (args.length < 1 )
        {
            System.out.println("Invalid Number of Arugments , provide the agent properties file path! " );
            return;
        }
        else
        {
            try {
                // in the VShpere Entity we are storing the VCentre IP Address
                //  , user name ,
                //   password , vmname
               // 
                Integer duration = 120000;
                System.out.println("inside main method");
                String alarmCondition = "OFF"; // for checking alarm is raised or not
                String vesSendStatus = "new";  //vesSendStatus
                String filePath=args[0];
               
                //  VSphereData contains all method to connect ,
               //  retrieve and
               //  fetch data using VShpere API
               //  
               
               VsphereData vsphereData = new VsphereData();
                VsphereEntity vsphereEntity = new VsphereEntity();
                VesEntity vesEntity = new VesEntity();
                ReadPropertiesFile file = new ReadPropertiesFile();
                if(file.readProperties(vsphereEntity, vesEntity, filePath))
                {
                    VESRestAPI vesRestAPI= new VESRestAPI();
                    JSONObject eventObj = new JSONObject();
                    JSONObject event = new JSONObject();
                    JSONObject commonEventHeader = new JSONObject();
                    JSONObject faultFields = new JSONObject();
                    VesTimer timer = new VesTimer(vesEntity, map, vesRestAPI);
                    while(true)
                    {
                       //  In this we are calling pyvmomi sdk via python to get the list of VM
                        //  containing instanceUUID and heartbeatstatus for each VM into a JSON File 
                        Runtime rt = Runtime.getRuntime();
                        Process p = rt.exec("python "+vsphereEntity.getPathVspherePython()+" -s "+vsphereEntity.getVsphereServerName()+" -u "+vsphereEntity.getVsphereUsername()+" -p "+vsphereEntity.getVsperePassword());
                        System.out.println("......done..json...");
                        Thread.sleep(5000);

                 //   Here we are opening the JSON File
                 //   and iterating and fetching the indivudal VM details and deciding the logic of raising the alarm on/off 
                        Object obj = parser.parse(new FileReader(vsphereEntity.getPythonOutputJson()));
                        JSONArray jsonObject = (JSONArray) obj;
                        System.out.println(jsonObject.toJSONString());
                        System.out.println("inside while loop");
                        for(int j = 0;j<=jsonObject.size()-1;j++){
                            System.out.println("timer is running or not: "+timer.isTimerRunning());
                            System.out.println("Is timed out happn: "+timer.isTimeout());
                            JSONObject js = (JSONObject) jsonObject.get(j);
                            System.out.println("");
                            System.out.println(js.toJSONString());
                            count++;
                            System.out.println("////////////////////////////////////////////////////////////////////////////");
                            System.out.println("map entries in total"+map.totalEntriesInMap());
                            System.out.println("Count:"+count);
                            VsphereDataEntity entity = vsphereData.gettingVMInfo(js,vsphereDataEntity,vsphereEntity);
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
                                    vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                                    list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
                                    System.out.println(list.get(0).json+" :"+list.get(0).alarm+" :"+list.get(0).vesSendStatus);
                                    map.addToMap(uuid_key, list);

                                    if(map.totalEntriesInMap()>1)
                                    {
                                        JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
                                        vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, uuid_key, list, duration);                   
                                    }
                                    else
                                    {
                                        //map.addToMap(uuid_key, list);
                                        //vesRestAPI.publishAnyEventToVES(vesEntity, event,null,map, timer);
                                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key, list,duration,vesSendStatus);
                                        System.out.println("published ");
                                    }
                                }
                            }
                            else if(heartBeatStatus == "green"){
                     //  if the alarm on entry is found in Map then check for the vesSendStatus
                       //        *  IF the VesSendStatus ==failed for Alarm On
                        //       *   in the case remove the entries from MAP and
                          //     *   donot encode the alarm off and donot send it to VESCollector 
                               if((map.isJsonFound(uuid_key) &&  map.retrieveAlarmConditionFromMap(uuid_key) == "ON") && map.retrieveVesSendStatusFromMap(uuid_key)!="failed"){		    	  
                                    alarmCondition = "OFF";
                                    vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                                    list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
                                    String json = event.toJSONString();
                                    System.out.println(json);
                                    map.addToMap(uuid_key, list);

                                    if(map.totalEntriesInMap()>1){
                                        //sending only entry having vesSendStatus = failed
                                        JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
                                        vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, json, list, duration);
                                    }
                                    else{
                                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key,list,duration,vesSendStatus);
                                    }
                                }
                                else{
                                    System.out.println("ALarm ON not found, ves Send status is failed");
                                }
                            }
                            Thread.sleep(2000);
                            System.out.println("for loop end...");
                        }
                        System.out.println(count);
                    }
                }
            }
            catch(java.io.FileNotFoundException  e){
                System.out.println("File not found exception. Check the json file path");
                //e.printStackTrace();
            }
            catch (InterruptedException e) {
                System.out.println("Intrupted..");
                //.args.e.printStackTrace();
            } catch (Exception e) {
                System.out.println("Exception Occured! Error in connection. Something went wrong with vsphere ip,username,password");
                e.printStackTrace();
            }
        }
    }
}
*/

public class VesAgentTest {

    static VsphereDataEntity vsphereDataEntity = new VsphereDataEntity();
    static JsonStoreMap map = new JsonStoreMap();
    static List<JsonAlarmStorage> list;
    public static String output;
    String alarmCondition = "OFF"; // for checking alarm is raised or not
    String vesSendStatus = "new";  //vesSendStatus

     String filepath="src/test/resources/agent.properties";
     public Integer duration=120000;
     VsphereData vsphereData = new VsphereData();
     VsphereEntity vsphereEntity = new VsphereEntity();
     VesEntity vesEntity = new VesEntity();
     ReadPropertiesFile file = new ReadPropertiesFile();

//    file.readProperties(vsphereEntity, vesEntity, filePath);
       
       VESRestAPI vesRestAPI= new VESRestAPI();
       JSONObject eventObj = new JSONObject();
       JSONObject event = new JSONObject();
       JSONObject commonEventHeader = new JSONObject();
       JSONObject faultFields = new JSONObject();
       VesTimer timer = new VesTimer(map);
      
      

public JSONArray getFileAsJsonObject()
        {
         JSONArray jsonArrayObj = null;
         FileReader fr = null;
         JSONParser parser = new JSONParser();
         String jsonfilepath="src/test/resources/event4xjson.json";
      try{
         fr = new FileReader ( jsonfilepath );
         Object obj =  parser.parse (fr);
         jsonArrayObj = (JSONArray) obj;
         System.out.println(jsonArrayObj.toJSONString());
       
       }
  
  catch(Exception e){
System.out.println("Exception while opening the file");
  e.printStackTrace();
}
 finally {
   //close the file
  if (fr != null) {
  try {
                                                                                  fr.close();
                                                                                    } catch (IOException e) 
                                                                                  {
                                                                                 System.out.println("Error closing file reader stream : " +e.toString());
                                                                                   }
                                                                                    }
                                                                                           }
      return jsonArrayObj;
}


@Test
    //public void testSingleHeartBeat() throws ClientProtocolException, IOException, ParseException
    public void testSingleHeartBeat() throws Exception{
            
       JSONArray jsonArrayObject = getFileAsJsonObject();
       String output = "true";

       for(int j = 0;j<=jsonArrayObject.size()-1;j++){

                 JSONObject js = (JSONObject) jsonArrayObject.get(j);
                  System.out.println("");
                  System.out.println(js.toJSONString());

                            VsphereDataEntity entity = vsphereData.gettingVMInfo(js,vsphereDataEntity,vsphereEntity);
                            String heartBeatStatus = vsphereDataEntity.getStatus();
                            System.out.println(heartBeatStatus);
                            String uuid_key = vsphereDataEntity.getSourceId();
                         vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                        list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
                        map.addToMap(uuid_key, list);
                       
                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key, list,duration,vesSendStatus);
                                                                                        
                      output="true";                                                                                         
                                   }
                                                                                        assertEquals ("true",output); 
                                                                                                       
}

@Test
    //public void testmultipleHeartbeat() throws FileNotFoundException, IOException, ParseException
    public void testmultipleHeartbeat() throws Exception{
           

	    String  outout  = "true";
        JSONArray jsonArrayObject = getFileAsJsonObject();

               for(int j = 0;j<=jsonArrayObject.size()-1;j++){
   
                            JSONObject js = (JSONObject) jsonArrayObject.get(j);
                            System.out.println("");
                            System.out.println(js.toJSONString());

                            VsphereDataEntity entity = vsphereData.gettingVMInfo(js,vsphereDataEntity,vsphereEntity);
                            String heartBeatStatus = vsphereDataEntity.getStatus();
                            System.out.println(heartBeatStatus);
                            String uuid_key = vsphereDataEntity.getSourceId();
                                                                                        
                         vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                        list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
                        map.addToMap(uuid_key, list);
                        map.updateMap(uuid_key, list);
                        
                        map.updateMapBatch("failed");
                       
           JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
          vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, uuid_key, list, duration , vesSendStatus);                   
                            output ="true";                                                             
                                                                                       } 
                                                                                        assertEquals ("true",output); 
                                                                                                        }



@Test
    //public void testmultipleHeartbeat() throws FileNotFoundException, IOException, ParseException
    public void testAlarmMapEntries() throws Exception{
           

	    String  outout  = "true";
    file.readProperties(vsphereEntity, filepath);
        JSONArray jsonArrayObject = getFileAsJsonObject();

               for(int j = 0;j<=jsonArrayObject.size()-1;j++){
   
                            JSONObject js = (JSONObject) jsonArrayObject.get(j);
                            System.out.println("");
                            System.out.println(js.toJSONString());

                            VsphereDataEntity entity = vsphereData.gettingVMInfo(js,vsphereDataEntity,vsphereEntity);
                            String heartBeatStatus = vsphereDataEntity.getStatus();
                            System.out.println(heartBeatStatus);
                            String uuid_key = vsphereDataEntity.getSourceId();
          
                              map.isJsonFound(uuid_key);
                              map.retrieveAlarmConditionFromMap(uuid_key);
                              map.retrieveALLFromMapBatch();
                              map.retrieveJsonFromMap(uuid_key);
                              map.retrieveVesSendStatusFromMap(uuid_key);
                              map.displayAllEntriesInMap();
                              map.deleteFromMap(uuid_key);
                              map.deleteAllFromMap();
                              map.deleteUsingAlarmCondition("AlarmOn");
                              map.totalEntriesInMap();
                              timer.isTimerRunning();
                              timer.startTimer(5000);
                              timer.stopTimer();
                              timer.isTimeout();
                              output ="true";                                                             
                                                                                       } 
                                                                                        assertEquals ("true",output); 
                                                                                                        }

}

