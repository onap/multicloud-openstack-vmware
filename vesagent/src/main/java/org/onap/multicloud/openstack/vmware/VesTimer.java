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
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;


class TimerExtend extends Timer{

    public TimerExtend(){
        VesTimer.hasStarted = true;
    }

    public boolean hasRunStarted() {
        return VesTimer.hasStarted;
    }
}

class TaskTimeout extends TimerTask{
   private static JsonStoreMap map;
   private final Logger log = LoggerFactory.getLogger(TaskTimeout.class);
  @SuppressWarnings("static-access")
   public TaskTimeout(JsonStoreMap map) {
      TaskTimeout.map = map;
   }
   
   public static void run1(){
       VesTimer.timeoutCheck = true;
       map.deleteAllFromMap();
       VesTimer.hasStarted=false;
    }
 @SuppressWarnings("resource")
 @Override
  public void run() {
      run1();
   log.info("In Time out before deleting the entries from Map");
 
   }
}

public class VesTimer {
    TimerExtend tt = null;
    TaskTimeout timeout = null;
    static boolean  hasStarted = false;
    static boolean timeoutCheck = false;
    private JsonStoreMap map;
    private final Logger log = LoggerFactory.getLogger(VesTimer.class);
    public VesTimer(JsonStoreMap map){
       this.map = map;
  }

    public void startTimer(Integer duration){
        tt = new TimerExtend();
        timeout= new TaskTimeout(this.map);
        log.info("timer started.................");
        tt.schedule(timeout, duration);
    }

    public void stopTimer(){
        tt.cancel();
        log.info("timer stopped");
    }

    public  boolean isTimerRunning(){
        if(VesTimer.hasStarted == true){
            log.info("timer started....");
            return true;
        }
       else {
          log.info("timer is not running");
          return false;
    }
}
    public String isTimeout(){
        if(VesTimer.timeoutCheck){
            log.info("expired");
            return "expired";
        }
    return "not expired";
    }
}
