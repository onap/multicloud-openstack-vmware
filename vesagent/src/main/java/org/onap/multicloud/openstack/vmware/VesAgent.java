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
   private static final Integer TIMERDURATION=360000;
   private static final String GREEN="green";
 private VesAgent(){
    }
    public static void main(String[] args) throws InterruptedException {
       BasicConfigurator.configure();
       if (args.length < 1 )
        {
            log.info("Invalid Number of Arugments , provide agent properties file path! " );
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
                        log.info("Excecuted python scipt. Json file created");
                        Thread.sleep(5000);
                        log.info("JSON File Path: " + vsphereEntity.getPythonOutputJson());
                        /* Here we are opening the JSON File
                        * and iterating and fetching the indivudal VM details and deciding the logic of raising the alarm on/off */
                        Object obj = parser.parse(new FileReader(vsphereEntity.getPythonOutputJson()));
                        JSONArray jsonObject = (JSONArray) obj;
                        log.info(jsonObject.toString());
                        log.info("Iterating Json files-vms");
                        for(int j = 0;j<=jsonObject.size()-1;j++){
                            log.info("Is timer running: ",timer.isTimerRunning());
                            log.info("Is timed out happen: ",timer.isTimeout());
                            JSONObject js = (JSONObject) jsonObject.get(j);
                            count++;
                            log.info("////////////////////////////////////////////////////////////////////////////");
                            log.info("Total entries in map:  ",map.totalEntriesInMap());
                            log.info("Count for checking vms :",count);
                            VsphereDataEntity entity = vsphereData.gettingVMInfo(js,vsphereDataEntity,vsphereEntity);
                            String heartBeatStatus = vsphereDataEntity.getStatus();
                            String uuidKey = vsphereDataEntity.getSourceId();
                            log.info("Heart beat status of vm",heartBeatStatus);
                            if(!heartBeatStatus.equals(GREEN)){
                                //encode json
                                if(map.isJsonFound(uuidKey) && map.retrieveFromMap(uuidKey, "ALARM") == "ON"){
                                    log.info("Alarm ON already raised...");
                                }
                                else if(!map.isJsonFound(uuidKey)){
                                    alarmCondition = "ON";
                                    vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                                    list = vsphereData.listJsonAlarm(event, alarmCondition,vesSendStatus);
                                    log.info("json, alarm and vesSend status:  "+list.get(0).json.toString()+" :"+list.get(0).alarm+" :"+list.get(0).vesSendStatus);
                                    map.addToMap(uuidKey, list);

                                    if(map.totalEntriesInMap()>1)
                                    {
                                        JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
                                        vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, uuidKey, list, TIMERDURATION,vesSendStatus);                   
                                    }
                                    else
                                    {
                                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuidKey, list,TIMERDURATION,vesSendStatus);
                                        log.info("published any event ");
                                    }
                                }
                            }
                            else if(heartBeatStatus.equals(GREEN)){                              /* if the alarm on entry is found in Map then check for the vesSendStatus
                               *  IF the VesSendStatus ==failed for Alarm On
                               *   in the case remove the entries from MAP and
                               *   donot encode the alarm off and donot send it to VESCollector */
                               if((map.isJsonFound(uuidKey) &&  map.retrieveFromMap(uuidKey, "ALARM") == "ON") && map.retrieveFromMap(uuidKey,"VES_STATUS")!="failed"){	
                                    log.info("heart beat status is green, uuid found in map ");
                                    alarmCondition = "OFF";
                                    vsphereData.encodeJson(entity, event, eventObj, commonEventHeader, faultFields,map);
                                    list = vsphereData.listJsonAlarm(event, alarmCondition,vesSendStatus);
                                    String json = event.toJSONString();
                                    map.addToMap(uuidKey, list);

                                    if(map.totalEntriesInMap()>1){
                                        //sending only entry having vesSendStatus = failed
                                        JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
                                        vesRestAPI.publishBatchEventToVES(vesEntity, alarmJsonConstructArray, map, timer, json, list, TIMERDURATION,vesSendStatus);
                                    }
                                    else{
                                        vesRestAPI.publishAnyEventToVES(vesEntity,map, timer,uuidKey,list,TIMERDURATION,vesSendStatus);
                                    }
                                }
                                else{
                                    log.info("ALarm ON not found for the VM");
                                }
                            }
                            Thread.sleep(2000);
                            log.info("End of iteration - for loop - vm");
                        }
                        }else if(result!=0){
                            log.info("Process terminated! python execution failed");
                         }
                         i++;
                        if (i  == Integer.MIN_VALUE) {  // true at Integer.MAX_VALUE +1
                            break;
                        }
                    }
                }else{
                     log.info("Error in Vsphere Credentials/python file path/json file path/- Set Env Variables properly ");
                 }
          } catch(java.io.FileNotFoundException  e){
                log.info("File not found exception. Check the json file path");
                log.error(ERROR,e);
            }
            catch (IOException e) {
                log.info("Something went wrong with python script - runtime");
                log.error(ERROR,e);
          } catch (InterruptedException e) {
                 Thread.currentThread().interrupt();
                log.info("Interupted exception occured. Python script execution taking more time");
               log.error(ERROR,e);

         } catch (ParseException e) {
                 log.info("Something went wrong with json created by python script! Parse exception occured");
                 log.error(ERROR,e);
          }catch (Exception e) {
               log.info("Exception occured!!");
               log.error(ERROR,e);

          } }
    }
    public static String getDateTime(){
        DateFormat df = DateFormat.getDateTimeInstance (DateFormat.MEDIUM, DateFormat.MEDIUM, new Locale ("en", "EN"));
        return df.format(new Date ());
 }


 public static boolean getEnv(VsphereEntity vsphereEntity, VesEntity vesEntity){
    try{
     if(System.getenv("Vsphere_Ip").isEmpty() || System.getenv("Vsphere_Username").isEmpty() || System.getenv("Vsphere_Password").isEmpty()){
       if(System.getenv("VesCollector_Ip").isEmpty() || System.getenv("VesCollector_Port").isEmpty()){
            log.info("Null values");
            return false;
        }
        }
        else{
           if(System.getenv("Vsphere_Password").length()==0 || System.getenv("Vsphere_Ip").length()==0 || System.getenv("Vsphere_Username").length() == 0){
               log.info("Vsphere credentials empty. Set env Var ...");
               return false;
           }
           vsphereEntity.setVsphereServerName(System.getenv("Vsphere_Ip"));
            vsphereEntity.setVsphereUsername(System.getenv("Vsphere_Username"));
            vsphereEntity.setVsperePassword(System.getenv("Vsphere_Password"));
            vesEntity.setVesip(System.getenv("VesCollector_Ip"));
            vesEntity.setVesPassword(System.getenv("VesCollector_Port"));
            return true;
        }
    }catch(NullPointerException e){
                log.error("Missing values -Set env var",e);
                }
                return false;
 }
}
