# Copyright (c) 2017-2018 VMware, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.

import os

# [MSB]
MSB_SERVICE_IP = '127.0.0.1'
MSB_SERVICE_PORT = '10080'

# [IMAGE LOCAL PATH]
ROOT_PATH = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

# [A&AI]
AAI_ADDR = os.getenv("AAI_ADDR", "aai.api.simpledemo.openecomp.org")
AAI_PORT = os.getenv("AAI_PORT", "8443")
AAI_SERVICE_URL = 'https://%s:%s/aai' % (AAI_ADDR, AAI_PORT)
AAI_SCHEMA_VERSION = "v13"
AAI_USERNAME = 'AAI'
AAI_PASSWORD = 'AAI'

# [DMaaP]
MR_ADDR = '127.0.0.1'
MR_PORT = '3904'

# [MDC]
SERVICE_NAME = "multicloud-vio"
FORWARDED_FOR_FIELDS = ["HTTP_X_FORWARDED_FOR", "HTTP_X_FORWARDED_HOST",
                        "HTTP_X_FORWARDED_SERVER"]

# [Local Config]
API_SERVER_PORT = 9004
