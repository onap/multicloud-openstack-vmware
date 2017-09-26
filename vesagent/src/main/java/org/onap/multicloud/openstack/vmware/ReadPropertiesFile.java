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


import java.io.File;
import java.io.FileInputStream;
import java.util.Properties;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class ReadPropertiesFile {
    private final Logger log = LoggerFactory.getLogger(ReadPropertiesFile.class);
    public boolean readProperties(VsphereEntity vsphereEntity,String filePath){
        try {
            File file = new File(filePath);
            FileInputStream fileInput = new FileInputStream(file);
            Properties properties = new Properties();
            properties.load(fileInput);
            fileInput.close();
            if( properties.getProperty("Path_VspherePython").isEmpty() || properties.getProperty("Python_Output_Json").isEmpty()){
                log.info("Provide  python path and json path in Agent.properties file");
                return false;
            }else{                
             vsphereEntity.setPathVspherePython(properties.getProperty("Path_VspherePython"));
            vsphereEntity.setPythonOutputJson(properties.getProperty("Python_Output_Json"));
            return true;
        }
        }
      catch(Exception e){
           log.info("Agent.properties file doen't have appropriate values or the file is empty Please modify Agent.properties!");
           log.error("error",e);
           
       }

        return false;
    }
}
