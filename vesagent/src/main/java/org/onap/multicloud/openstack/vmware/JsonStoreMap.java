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
/*JsonStoreMap class having all methods
 *  related with HashMap
 *  Map taking UUID of VM as key
 *  Value is List Contain encoded json, alarm condition
 *  and ves send status
 *  If need to add any values --> add to JsonStoreMap */

public class JsonStoreMap {
    protected static final Map<String, List<JsonAlarmStorage>> map = new HashMap<String, List<JsonAlarmStorage>>();

    public Map<String, List<JsonAlarmStorage>> addToMap(String key,List<JsonAlarmStorage> value){
        System.out.println("adding to map");
        map.put(key, value);
        return map;
    }
    public Map<String, List<JsonAlarmStorage>> UpdateMap(String key,List<JsonAlarmStorage> value){
        System.out.println("updating map");
    /*if(map.containsKey(key)){
    map.remove(key);
    }*/
        map.put(key, value);
        return map;
      }
    public Map<String, List<JsonAlarmStorage>> UpdateMapBatch(String vesSendStatus){
       System.out.println("updating map for batch");
        Iterator i = map.keySet().iterator();
        while(i.hasNext())
        {
            String key = i.next().toString();
            List<JsonAlarmStorage> value = map.get(key);
            value.get(0).vesSendStatus = vesSendStatus;
        }
        System.out.println("updated total batch with  vesSendStatus = 'failed'");
        return map;
    }
    public String retrieveFromMap(String key){
        List<JsonAlarmStorage> value;
        System.out.println("retriving json from map");
        if (map.containsKey(key)) {
            value = map.get(key);
            System.out.println(value.size());
            System.out.println("Key : " + key +" value :"+ value.get(0).alarm+""+value.get(0).json);
            return value.get(0).json.toString();
        }
        return "nothing";
    }

    public String retrieveAlarmConditionFromMap(String key){
        List<JsonAlarmStorage> value;
        System.out.println("retriving alarm condition from map");
        if (map.containsKey(key)) {
            value = map.get(key);
            //System.out.println("Key : " + key +" value :"+ value);
            return value.get(0).alarm;
        }
        return "uuid not found";
    }

    public String retrieveVesSendStatusFromMap(String key){
        List<JsonAlarmStorage> value;
        System.out.println("retriving alarm condition from map");
        if (map.containsKey(key)) {
            value = map.get(key);
            //System.out.println("Key : " + key +" value :"+ value);
            return value.get(0).vesSendStatus;
        }
        return "uuid not found";
    }

    public JSONObject retrieveJsonFromMap(String key){
        List<JsonAlarmStorage> value;
        System.out.println("retriving json from map");
        if (map.containsKey(key)) {
            value = map.get(key);
            //System.out.println("Key : " + key +" value :"+ value);
            return value.get(0).json;
        }
        return null;
    }

    @SuppressWarnings({ "rawtypes", "unchecked" })
    public JSONObject retrieveALLFromMapBatch(){
        System.out.println("Encoding and retriving json for batch");
        JSONObject eventList = new JSONObject();
        JSONArray list = new JSONArray();
        Iterator i = map.keySet().iterator();
        while(i.hasNext())
        {
            String key = i.next().toString();
            List<JsonAlarmStorage> value = map.get(key);
            System.out.println("Key : " + key +" value :"+ value.get(0).alarm+""+value.get(0).json);
            JSONObject json = value.get(0).json;
            System.out.println(".........................");
            System.out.println(json.get("event"));
            JSONObject obj = (JSONObject) json.get("event");
            list.add(obj);
        }
        System.out.println(".........................");
        eventList.put("eventList", list);
        System.out.println(eventList);
        System.out.println(".........................");
        return eventList;
    }


    @SuppressWarnings("rawtypes")
    public void retrieveALLFromMap(){
        System.out.println("retrive all from map");
        Iterator i = map.keySet().iterator();
        String mapValues = null;
        while(i.hasNext()){
            String key = i.next().toString();
            List<JsonAlarmStorage> value = map.get(key);
            mapValues = "uuid: "+key+" jsonStructure: "+value.get(0).json.toString()+" AlarmCondition: "+value.get(0).alarm+": VesSend status: "+value.get(0).vesSendStatus;	
            System.out.println(mapValues);
        }
    }

    public void deleteFromMap(String key){
        System.out.println("deleting json from map");
        map.remove(key);
        System.out.println("values of key "+key+" deleted successfully");
    }

  @SuppressWarnings("rawtypes")
public void deleteUsingAlarmCondition(String alarm){
    Iterator it = map.entrySet().iterator();
    while (it.hasNext())
    {
        Entry item = (Entry) it.next();
        System.out.println(item.getKey());;
        List<JsonAlarmStorage> value = map.get(item.getKey());
        if(value.get(0).alarm == alarm)
        {
            System.out.println("Key : " + item.getKey() +" value :"+ value.get(0).alarm+""+value.get(0).json);
            it.remove();
            System.out.println("removed..");
        }
    }
    System.out.println("removed");
}




    public void deleteAllFromMap(){
        System.out.println("clearing map");
        map.clear();
        System.out.println("map cleared..");
        System.out.println(map.toString());
    }

    public int totalEntriesInMap(){
        System.out.println("map size");
        return map.size();
    }

    public boolean isJsonFound(String key){
        System.out.println("checking uuid in map");
        if(map.containsKey(key))
        {
            return true;
        }
        return false;
    }
}
