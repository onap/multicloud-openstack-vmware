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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.apache.log4j.BasicConfigurator;
public class VesAgent {
  private static final Logger log = LoggerFactory.getLogger(VesAgent.class);
  private static final String ERROR = "error";
  private VesAgent(){
 
  } 
  public static void main (String[] args ) throws InterruptedException {
     BasicConfigurator.configure(); 

 if (args.length < 1 )
  {
       log.info("Invalid Number of Arugments , provide the agent properties file path! " );
       return;
  }
  else
  {
      try {
     /* in the VShpere Entity we are storing the VCentre IP Address
      *  , user name ,
      *  password , vmname
     */

    int count = 0;
    VsphereDataEntity vsphereDataEntity = new VsphereDataEntity();
    JsonStoreMap map = new JsonStoreMap();
    List<JsonAlarmStorage> list;
    JSONParser parser = new JSONParser();
    Integer duration = 120000;
    log.info("inside main method");
    String alarmCondition; // for checking alarm is raised or not
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
     if(file.readProperties(vsphereEntity,filePath) && getEnv(vsphereEntity, vesEntity))
       {
         VESRestAPI vesRestAPI= new VESRestAPI();
         JSONObject eventObj = new JSONObject();
          JSONObject event = new JSONObject();
          JSONObject commonEventHeader = new JSONObject();
          JSONObject faultFields = new JSONObject();
          VesTimer timer = new VesTimer(map);
                   int i=0;
                   while(true)
                    {
                        /* In this we are calling pyvmomi sdk via python to get the list of VM
                        * containing instanceUUID and heartbeatstatus for each VM into a JSON File */
                        log.info("timer before running python"+getDateTime());
                        Runtime rt = Runtime.getRuntime();
                        log.info("Execute Python File: " + vsphereEntity.getPathVspherePython());
                        Process p = rt.exec("python "+vsphereEntity.getPathVspherePython()+" -s "+vsphereEntity.getVsphereServerName()+" -u "+vsphereEntity.getVsphereUsername()+" -p "+vsphereEntity.getVsperePassword());
                        int result=p.waitFor();
                        if(result == 0){
                        System.out.println("......done..json...");
                        Thread.sleep(5000);
			log.info("JSON File Path: " + vsphereEntity.getPythonOutputJson());
                        /* Here we are opening the JSON File
                        * and iterating and fetching the indivudal VM details and deciding the logic of raising the alarm on/off */
                        Object obj = parser.parse(new FileReader(vsphereEntity.getPythonOutputJson()));
                        JSONArray jsonObject = (JSONArray) obj;
                        log.info(jsonObject.toJSONString());
                        log.info("inside while loop");
                        for(int j = 0;j<=jsonObject.size()-1;j++){
                            log.info("timer is running or not: "+timer.isTimerRunning());
                            log.info("Is timed out happn: "+timer.isTimeout());
                            JSONObject js = (JSONObject) jsonObject.get(j);
                            log.info("");
                            log.info(js.toJSONString());
                            count++;
                            log.info("////////////////////////////////////////////////////////////////////////////");
                            log.info("map entries in total"+map.totalEntriesInMap());
                            log.info("Count:"+count);
                            VsphereDataEntity entity = vsphereData.gettingVMInfo(js,vsphereDataEntity,vsphereEntity);
                            String heartBeatStatus = vsphereDataEntity.getStatus();
                            log.info(heartBeatStatus);

                            String uuid_key = vsphereDataEntity.getSourceId();
                            if(heartBeatStatus!="green"){
                                //encode json
                                if(map.isJsonFound(uuid_key) && map.retrieveAlarmConditionFromMap(uuid_key) == "ON"){
                                    log.info("alarm ON already raised");
                                }
                                else if(!map.isJsonFound(uuid_key)){
                                    alarmCondition = "ON";
                                    vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                                    list = vsphereData.listJsonAlarm2(event, alarmCondition,vesSendStatus);
                                    log.info(list.get(0).json+" :"+list.get(0).alarm+" :"+list.get(0).vesSendStatus);
                                    map.addToMap(uuid_key, list);

                                    if(map.totalEntriesInMap()>1)
                                    {
                                        JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
                                        vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, uuid_key, list, duration , vesSendStatus);                   
                                    }
                                    else
                                    {
                                        //map.addToMap(uuid_key, list);
                                        //vesRestAPI.publishAnyEventToVES(vesEntity, event,null,map, timer);
                                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key, list,duration,vesSendStatus);
                                        log.info("published ");
                                        
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
                                    log.info(json);
                                    map.addToMap(uuid_key, list);

                                    if(map.totalEntriesInMap()>1){
                                        //sending only entry having vesSendStatus = failed
                                        JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
                                        vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, json, list, duration,vesSendStatus);
                                    }
                                    else{
                                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuid_key,list,duration,vesSendStatus);
                                    }
                                }
                                else{
                                    log.info("ALarm ON not found, ves Send status is failed");
                                }
                            }
                            Thread.sleep(2000);
                            log.info("for loop end...");
                        }
                        log.info(String.valueOf(count));

                        }else if(result!=0){
                            log.info("Something went wrong on fetching info using python script!! Check the python script and credentials");
                            break;
                         }
                         i++;
                        if (i  == Integer.MIN_VALUE) {  // true at Integer.MAX_VALUE +1
                            break;
                        }
                    }
                }else{
                     log.info("Missing values for python files - Env Variabl    es ");

            }
         }   catch(java.io.FileNotFoundException  e){
                log.info("File not found exception. Check the json file path");
                log.error(ERROR,e); 
            }
            catch (IOException e) {
                log.info("Something went wrong with python in runtime");
                log.error(ERROR,e); 
          } catch (InterruptedException e) {
                 Thread.currentThread().interrupt();
                 log.info("Interupted exception occured. Python script execution taking more time");
                log.error(ERROR,e); 
          } catch (ParseException e) {
                 log.info("Something went wrong with json created by python! Parse exception occured");
                log.error(ERROR,e); 
          }catch (Exception e) {
                log.info("Exception Occured!!");
                log.error(ERROR,e); 
          } }
    }
    public static String getDateTime(){
        DateFormat df = DateFormat.getDateTimeInstance (DateFormat.MEDIUM, DateFormat.MEDIUM, new Locale ("en", "EN"));
        return df.format (new Date ());
     }
public static boolean getEnv(VsphereEntity vsphereEntity, VesEntity vesEntity){
    try{
     if(System.getenv("Vsphere_Ip").isEmpty() || System.getenv("Vsphere_Username").isEmpty() || System.getenv("Vsphere_Password")==null || System.getenv("VesCollector_Ip").isEmpty() || System.getenv("VesCollector_Port").isEmpty()){
      log.info("Null values");
      return false;
  }
  else{
      vsphereEntity.setVsphereServerName(System.getenv("Vsphere_Ip"));
      vsphereEntity.setVsphereUsername(System.getenv("Vsphere_Username"));
      vsphereEntity.setVsperePassword(System.getenv("Vsphere_Password"));
      vesEntity.setVesip(System.getenv("VesCollector_Ip"));
      vesEntity.setVesPassword(System.getenv("VesCollector_Port"));
      return true;

     }
  }catch(NullPointerException e){
               log.error("Missing values - env var",e);
               }
               return false; 
  }
}
