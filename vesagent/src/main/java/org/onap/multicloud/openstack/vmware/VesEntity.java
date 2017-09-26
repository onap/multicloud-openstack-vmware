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
/*Entity class for ves ip
 * port
 * username
 * password*/
public class VesEntity {
    private String vesip;
    private Integer port;
    private String vesUsername;
    private String vesPassword;
    public String getVesip() {
	    return vesip;
    }
    public void setVesip(String vesip) {
        this.vesip = vesip;
    }
    public Integer getPort() {
        return port;
    }
    public void setPort(Integer port) {
        this.port = port;
    }
    public String getVesUsername() {
        return vesUsername;
    }
    public void setVesUsername(String vesUsername) {
        this.vesUsername = vesUsername;
    }
    public String getVesPassword() {
        return vesPassword;
    }
    public void setVesPassword(String vesPassword) {
        this.vesPassword = vesPassword;
    }
}
