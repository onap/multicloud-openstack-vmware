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
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.Properties;

public class ReadPropertiesFile {
    
    public boolean readProperties(VsphereEntity vsphereEntity,VesEntity vesEntity,String filePath){
        try {
            File file = new File(filePath);
            FileInputStream fileInput = new FileInputStream(file);
            Properties properties = new Properties();
            properties.load(fileInput);
            fileInput.close();
            if(properties.getProperty("Vsphere_Ip").isEmpty() || properties.getProperty("Vsphere_Username").isEmpty() || properties.getProperty("Vsphere_Password").isEmpty() || properties.getProperty("Path_VspherePython").isEmpty()){
                System.out.println("Provide username/password/ip  in Agent.properties file");
            }
            vsphereEntity.setVsphereServerName(properties.getProperty("Vsphere_Ip"));
            vsphereEntity.setVsphereUsername(properties.getProperty("Vsphere_Username"));
            vsphereEntity.setVsperePassword(properties.getProperty("Vsphere_Password"));
            vesEntity.setVesip(properties.getProperty("VesCollector_Ip"));
            vesEntity.setVesUsername(properties.getProperty("VesCollector_Username"));
            vesEntity.setVesPassword(properties.getProperty("VesCollector_Password"));
            vesEntity.setPort(Integer.parseInt(properties.getProperty("VesCollector_Port")));
            vsphereEntity.setPathVspherePython(properties.getProperty("Path_VspherePython"));
            vsphereEntity.setPythonOutputJson(properties.getProperty("Python_Output_Json"));
            return true;
        } catch (FileNotFoundException e) {
            System.out.println("Property file is missing.. provide file");
            //e.printStackTrace();
        } catch (IOException e) {
            //e.printStackTrace();
        }catch (java.lang.NumberFormatException e) {
            System.out.println("Agent.properties file doen't have appropriate values!");
        }
        catch (java.lang.NullPointerException e) {
            System.out.println("Agent.properties file doen't have appropriate values or the file is empty Please modify Agent.properties!");
        }
        return false;
    }
}
