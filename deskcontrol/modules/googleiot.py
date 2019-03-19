# Copyright 2017 Google Inc. / Arup
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Modified from the Python sample for connecting to Google Cloud IoT Core
# Original source: https://github.com/GoogleCloudPlatform/python-docs-samples/
#              blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py

# Subscribe/Callback Docs https://eclipse.org/paho/clients/python/docs/

from mqtt_module import MQTTModule
from datetime import datetime, timedelta
import jwt
from config import *



class GoogleIoTModule(MQTTModule):

    @property
    def publish_topic(self):
        return '/devices/{}/events'.format(GCLOUD_CONFIG['device_id'])

    @property
    def subscribe_topic(self):
        return '/devices/{}/events/commands'.format(GCLOUD_CONFIG['device_id'], 1)

    @property
    def username(self):
        return 'unused'

    @property
    def client_id(self):
        return 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            GCLOUD_CONFIG['project_id'],
            GCLOUD_CONFIG['cloud_region'],
            GCLOUD_CONFIG['registry_id'],
            GCLOUD_CONFIG['device_id'])

    @property
    def password(self):
        return self.create_jwt(
            GCLOUD_CONFIG['project_id'],
            GCLOUD_CONFIG['private_key_file'],
            GCLOUD_CONFIG['algorithm']
        )

    @property
    def mqtt_host_name(self):
        return GCLOUD_CONFIG['mqtt_bridge_hostname']

    @property
    def mqtt_port(self):
        return GCLOUD_CONFIG['mqtt_bridge_port']

    def set_tls(self, client):
        client.tls_set(ca_certs=GCLOUD_CONFIG['ca_certs'])


    def create_jwt(self, project_id, private_key_file, algorithm):
        token = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'aud': project_id
        }

        with open(private_key_file, 'r') as f:
            private_key = f.read()

        return jwt.encode(token, private_key, algorithm=algorithm)
