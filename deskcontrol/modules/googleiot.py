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

from navigation import StateModule
from datetime import datetime, timedelta
import jwt
import json
import paho.mqtt.client as mqtt
from config import GCLOUD_CONFIG


class GoogleIoTModule(StateModule):
    client = None
    always_tick = True

    def __init__(self, controller):
        super(GoogleIoTModule, self).__init__(controller)
        args = GCLOUD_CONFIG
        self.client = mqtt.Client(
            client_id=(
                'projects/{}/locations/{}/registries/{}/devices/{}'.format(
                    args['project_id'],
                    args['cloud_region'],
                    args['registry_id'],
                    args['device_id'])))

        self.client.username_pw_set(
            username='unused',
            password=self.create_jwt(
                args['project_id'],
                args['private_key_file'],
                args['algorithm']))

        self.client.tls_set(ca_certs=args['ca_certs'])

        self.client.connect(
            args['mqtt_bridge_hostname'],
            args['mqtt_bridge_port'])

        self.client.loop_start()

        self.mqtt_topic = '/devices/{}/events'.format(args['device_id'])

    def publish(self, controller, key, value, tags={}):
        try:
            ident = self.controller.identity
            payload = json.dumps({
                "measurement": str(ident + "_" + key),
                "time": (
                    datetime.utcnow().replace(microsecond=0).isoformat() +
                    "Z"),
                "tags": tags,
                "fields": {"value": value, }
            })
            print('Publishing message: \'{}\''.format(payload))
            self.client.publish(self.mqtt_topic, payload, qos=1)
        except Exception as e:
            print("Error publishing to GCloud:")
            print(e)

    def tick(self):
        if self.client and "SensorModule" in self.controller.modules:
            for key in self.controller.modules["SensorModule"].sensors:
                sensor = self.controller.modules["SensorModule"].sensors[key]
                if sensor.updated < (datetime.now() -
                                     timedelta(minutes=1)):
                    sensor.get_value()

    def create_jwt(self, project_id, private_key_file, algorithm):
        token = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'aud': project_id
        }

        with open(private_key_file, 'r') as f:
            private_key = f.read()

        return jwt.encode(token, private_key, algorithm=algorithm)
