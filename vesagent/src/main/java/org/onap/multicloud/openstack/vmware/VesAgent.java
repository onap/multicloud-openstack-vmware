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

import java.io.FileReader;
import java.util.List;
import java.text.DateFormat;
import java.util.Date;
import java.util.Locale;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;
import java.io.IOException;
public class VesAgent {
    static int count = 0;
    static VsphereDataEntity vsphereDataEntity = new VsphereDataEntity();
    static JsonStoreMap map = new JsonStoreMap();
    static List<JsonAlarmStorage> list;
    static JSONParser parser = new JSONParser();

    public static void main(String[] args) throws InterruptedException {
        if (args.length < 1 )
        {
            System.out.println("Invalid Number of Arugments , provide the agent properties file path! " );
            return;
        }
        else
        {
            try {
                /* in the VShpere Entity we are storing the VCentre IP Address
                *  , user name ,
                *  password , vmname
                */
                Integer duration = 120000;
                System.out.println("inside main method");
                String alarmCondition = "OFF"; // for checking alarm is raised or not
                String vesSendStatus = "new";  //vesSendStatus
                String filePath=args[0];
                /* VSphereData contains all method to connect ,
                * retrieve and
                * fetch data using VShpere API
                */
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
                   int i=0;
                   while(true)
                    {
                        /* In this we are calling pyvmomi sdk via python to get the list of VM
                        * containing instanceUUID and heartbeatstatus for each VM into a JSON File */
                        System.out.println("timer before running python"+getDateTime());
                        Runtime rt = Runtime.getRuntime();
                        System.out.println("Execute Python File: " + vsphereEntity.getPathVspherePython());
                        Process p = rt.exec("python "+vsphereEntity.getPathVspherePython()+" -s "+vsphereEntity.getVsphereServerName()+" -u "+vsphereEntity.getVsphereUsername()+" -p "+vsphereEntity.getVsperePassword());
                        int result=p.waitFor();
                        if(result == 0){
                        System.out.println("......done..json...");
                        Thread.sleep(5000);
			System.out.println("JSON File Path: " + vsphereEntity.getPythonOutputJson());
                        /* Here we are opening the JSON File
                        * and iterating and fetching the indivudal VM details and deciding the logic of raising the alarm on/off */
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
                               /* if the alarm on entry is found in Map then check for the vesSendStatus
                               *  IF the VesSendStatus ==failed for Alarm On
                               *   in the case remove the entries from MAP and
                               *   donot encode the alarm off and donot send it to VESCollector */
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

                        }else if(result!=0){
                            System.out.println("Something went wrong on fetching info using python script!! Check the python script and credentials");
                            break;
                         }
                         i++;
                        if (i  == Integer.MIN_VALUE) {  // true at Integer.MAX_VALUE +1
                            break;
                        }
                    }
                }
            }
            catch(java.io.FileNotFoundException  e){
                System.out.println("File not found exception. Check the json file path");
                //e.printStackTrace();
            }
            catch (IOException e) {
                System.out.println("Something went wrong with python in runtime");
          } catch (InterruptedException e) {
                 Thread.currentThread().interrupt();
                System.out.println("Interupted exception occured. Python script execution taking more time");
          } catch (ParseException e) {
                 System.out.println("Something went wrong with json created by python! Parse exception occured");
          }catch (Exception e) {
               System.out.println();
          } }
    }
    public static String getDateTime(){
        DateFormat df = DateFormat.getDateTimeInstance (DateFormat.MEDIUM, DateFormat.MEDIUM, new Locale ("en", "EN"));
        String formattedDate = df.format (new Date ());
        return formattedDate;
     }
}
