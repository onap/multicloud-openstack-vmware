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

public class VsphereEntity {
	public String VsphereServerName;
	public String VsphereUsername;
	public String VsperePassword;
	public String VsphereVMname;
	public String getVsphereUsername() {
		return VsphereUsername;
	}
	public void setVsphereUsername(String vsphereUsername) {
		VsphereUsername = vsphereUsername;
	}
	
	public String getVsperePassword() {
		return VsperePassword;
	}
	public void setVsperePassword(String vsperePassword) {
		VsperePassword = vsperePassword;
	}
	public String getVsphereVMname() {
		return VsphereVMname;
	}
	public void setVsphereVMname(String vsphereVMname) {
		VsphereVMname = vsphereVMname;
	}
	public String getVsphereServerName() {
		return VsphereServerName;
	}
	public void setVsphereServerName(String vsphereServerName) {
		VsphereServerName = vsphereServerName;
	}
	

}
