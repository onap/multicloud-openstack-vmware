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

import java.io.IOException;
import java.net.Socket;
import java.util.Timer;
import java.util.TimerTask;
import org.json.simple.JSONObject;
import org.json.simple.parser.ParseException;

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

        VesTimer.timeoutCheck = 1;
        System.out.println("time out");
        try {
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
        }
    }
}

public class VesTimer {
    public static TimerExtend tt = null;
    public static TaskTimeout timeout = null;
    public static boolean  hasStarted = false;
    public static int timeoutCheck = 0;
    private VesEntity ves;
    private JsonStoreMap map;
    private VESRestAPI vesRestAPI;

    public VesTimer(VesEntity ves, JsonStoreMap map, VESRestAPI vesRestAPI){
        this.ves = ves;
        this.map = map;
        this.vesRestAPI = vesRestAPI;
        tt = new TimerExtend();
        timeout= new TaskTimeout(this.ves,this.map,this.vesRestAPI);
    }

    public void startTimer(Integer duration){
        System.out.println("timer started.................");
        tt.schedule(timeout, duration);
    }

    public void stopTimer(){
        tt.cancel();
    System.out.println("timer stopped");
    }

    public  boolean isTimerRunning(){
        if(tt.hasRunStarted()==true){
            System.out.println("timer is running");
            return true;
        }
    return false;
    }

    public String isTimeout(){
        if(VesTimer.timeoutCheck == 1){
            System.out.println("expired");
            return "expired";
        }
    return "not expired";
    }
}
