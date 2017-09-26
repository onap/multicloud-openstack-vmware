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

import java.util.Timer;
import java.util.TimerTask;


class TimerExtend extends Timer{

    public TimerExtend(){
        VesTimer.hasStarted = true;
    }

    public boolean hasRunStarted() {
        return VesTimer.hasStarted;
    }
}

class TaskTimeout extends TimerTask{
    private VesEntity ves;
    private JsonStoreMap map;
    private VESRestAPI vesRestAPI;

    public TaskTimeout(VesEntity ves, JsonStoreMap map, VESRestAPI vesRestAPI) {
        this.ves = ves;
        this.map = map;
        this.vesRestAPI = vesRestAPI;
    }

    @SuppressWarnings("resource")
    @Override
    public void run() {

       VesTimer.timeoutCheck = true;
       System.out.println("In Time out before deleting the entries from Map");
       map.deleteAllFromMap();
       System.out.println("timed out");
       VesTimer.hasStarted = false;
        /*try {
           Socket sock = new Socket(ves.getVesip(), ves.getPort());
           if(sock.isConnected()){
            System.out.println("Encoded json and publishing batch event");
            JSONObject alarmJsonConstructArray = map.retrieveALLFromMapBatch();
            vesRestAPI.publishBatchEventToVES(ves, alarmJsonConstructArray);
           }
            VesTimer.timeoutCheck = 1;
            System.out.println("time out");
        }catch (IOException | ParseException e) {
            System.out.println("Connection Refused Error while send batch event");
            e.printStackTrace();
        }*/

    }
}

public class VesTimer {
    public static TimerExtend tt = null;
    public static TaskTimeout timeout = null;
    public static boolean  hasStarted = false;
    public static boolean timeoutCheck = false;
    private VesEntity ves;
    private JsonStoreMap map;
    private VESRestAPI vesRestAPI;

    public VesTimer(VesEntity ves, JsonStoreMap map, VESRestAPI vesRestAPI){
        this.ves = ves;
        this.map = map;
        this.vesRestAPI = vesRestAPI;
    }

    public void startTimer(Integer duration){
        tt = new TimerExtend();
        timeout= new TaskTimeout(this.ves,this.map,this.vesRestAPI);
        System.out.println("duration of timer: "+duration);
        System.out.println("timer started.................");
        tt.schedule(timeout, duration);
    }

    public void stopTimer(){
        tt.cancel();
        System.out.println("timer stopped");
    }

    public  boolean isTimerRunning(){
        if(VesTimer.hasStarted == true){
            System.out.println("timer started....");
            return true;
        }
       else {
          System.out.println("timer is not running");
          return false;
    }
}
    public String isTimeout(){
        if(VesTimer.timeoutCheck == true){
            System.out.println("expired");
            return "expired";
        }
    return "not expired";
    }
}
