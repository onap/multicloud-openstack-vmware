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

import org.json.simple.JSONObject;

/*JsonAlarmStorage class include
 * fields to stote to list
 * which will be the value of Map*/

public class JsonAlarmStorage {
     JSONObject json;
     String alarm;
     String vesSendStatus;
}
