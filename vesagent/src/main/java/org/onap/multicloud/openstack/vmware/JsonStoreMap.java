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

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
/*JsonStoreMap class having all methods
 *  related with HashMap
 *  Map taking UUID of VM as key
 *  Value is List Contain encoded json, alarm condition
 *  and ves send status
 *  If need to add any values --> add to JsonStoreMap */

public class JsonStoreMap {
    protected static final Map<String, List<JsonAlarmStorage>> map = new HashMap<>();
    private final Logger log = LoggerFactory.getLogger(JsonStoreMap.class);
    private String line = "......................";
    public Map<String, List<JsonAlarmStorage>> addToMap(String key,List<JsonAlarmStorage> value){
        log.info("adding to map");
        map.put(key, value);
        return map;
    }
    public Map<String, List<JsonAlarmStorage>> updateMap(String key,List<JsonAlarmStorage> value){
       log.info("updating the Map");
       map.put(key, value);
       return map;
      }
    public Map<String, List<JsonAlarmStorage>> updateMapBatch(String vesSendStatus){
        log.info("updating the map for batch");
        Iterator i = map.keySet().iterator();
        while(i.hasNext())
        {
            String key = i.next().toString();
            List<JsonAlarmStorage> value = map.get(key);
            value.get(0).vesSendStatus = vesSendStatus;
        }
        log.info("updated total batch with  vesSendStatus = 'failed'");
        return map;
    }

    public String retrieveFromMap(String key, String type){
        List<JsonAlarmStorage> value;
        log.info("retriving alarm condition from map");
        if (map.containsKey(key)) {
            value = map.get(key);
            if(type=="ALARM"){
                return value.get(0).alarm;
            }else if(type=="VES_STATUS"){
                return value.get(0).vesSendStatus;
            }
        }
        return null;
    }

    public JSONObject retrieveJsonFromMap(String key){
        List<JsonAlarmStorage> value;
        log.info("retriving json from map");
        if (map.containsKey(key)) {
            value = map.get(key);
            return value.get(0).json;
        }
        return null;
    }

    @SuppressWarnings({ "rawtypes", "unchecked" })
    public JSONObject retrieveALLFromMapBatch(){
        log.info("Encoding and retriving json for batch");
        JSONObject eventList = new JSONObject();
        JSONArray list = new JSONArray();
        Iterator i = map.keySet().iterator();
        while(i.hasNext())
        {
            String key = i.next().toString();
            List<JsonAlarmStorage> value = map.get(key);
            String value1=value.get(0).alarm+""+value.get(0).json.toString();
            log.info("Key : " + key +" value :"+value1);
            JSONObject json = value.get(0).json;
            log.info(line);
            log.info(json.get("event").toString());
            JSONObject obj = (JSONObject) json.get("event");
            list.add(obj);
        }
        log.info(line);
        eventList.put("eventList", list);
        log.info(eventList.toString());
        log.info(line);
        return eventList;
    }


    @SuppressWarnings("rawtypes")
    public void displayALLEntriesInMap(){
        log.info("retrive all the entries from map");
        Iterator i = map.keySet().iterator();
        String mapValues;
        while(i.hasNext()){
            String key = i.next().toString();
            List<JsonAlarmStorage> value = map.get(key);
            mapValues = "uuid: "+key+" jsonStructure: "+value.get(0).json.toString()+" AlarmCondition: "+value.get(0).alarm+": VesSend status: "+value.get(0).vesSendStatus;	
            log.info(mapValues);
        }
    }

    public void deleteFromMap(String key){
        log.info("deleting json from map");
        map.remove(key);
        log.info("values of key "+key+" deleted successfully");
    }

  @SuppressWarnings("rawtypes")
    public void deleteUsingAlarmCondition(String alarm){
        Iterator it = map.entrySet().iterator();
        while (it.hasNext()){
            Entry item = (Entry) it.next();
            List<JsonAlarmStorage> value = map.get(item.getKey());
            if(value.get(0).alarm == alarm){
                it.remove();
                log.info("removed..");
            }
        }
        log.info("removed");
    }

    public void deleteAllFromMap(){
       log.info("clearing map...");
        map.clear();
        log.info("map cleared...");
        log.info(map.toString());
    }

    public int totalEntriesInMap(){
        log.info("Total entries in map",map.size());
        return map.size();
    }

    public boolean isJsonFound(String key){
        log.info("checking uuid in map");
        if(map.containsKey(key))
        {
            return true;
        }
        return false;
    }
}
