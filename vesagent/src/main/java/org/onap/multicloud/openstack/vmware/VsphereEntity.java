 /* Copyright (c) 2017-2018 VMware, Inc.
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

public class VsphereEntity {
    private String vsphereServerName;
    private String vsphereUsername;
    private String vsperePassword;
    private String vsphereVMname;
    private String pathVspherePython;
    private String pythonOutputJson;

    public String getVsphereServerName() {
            return vsphereServerName;
    }
    public void setVsphereServerName(String vsphereServerName) {
            this.vsphereServerName = vsphereServerName;
    }
    public String getVsphereUsername() {
            return vsphereUsername;
    }
    public void setVsphereUsername(String vsphereUsername) {
            this.vsphereUsername = vsphereUsername;
    }
    public String getVsperePassword() {
            return vsperePassword;
    }
    public void setVsperePassword(String vsperePassword) {
            this.vsperePassword = vsperePassword;
    }
    public String getVsphereVMname() {
            return vsphereVMname;
    }
    public void setVsphereVMname(String vsphereVMname) {
            this.vsphereVMname = vsphereVMname;
    }
    public String getPathVspherePython() {
            return pathVspherePython;
    }
    public void setPathVspherePython(String pathVspherePython) {
            this.pathVspherePython = pathVspherePython;
    }
    public String getPythonOutputJson() {
            return pythonOutputJson;
    }
    public void setPythonOutputJson(String pythonOutputJson) {
            this.pythonOutputJson = pythonOutputJson;
    }
}
