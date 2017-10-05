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

from navigation import StateModule
from datetime import datetime, timedelta
import jwt
import json
import paho.mqtt.client as mqtt
from config import GCLOUD_CONFIG


class GoogleIoTModule(StateModule):
    client = None

    def __init__(self, controller):
        super(GoogleIoTModule, self).__init__(controller)
        controller.publishers.append(self.publish)
        self.mqtt_topic = '/devices/{}/events'.format(
            GCLOUD_CONFIG['device_id'])
        self.connect()

    def on_message(self, userdata, message):
        print(userdata, message)

    def connect(self):
        try:
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

            self.client.on_message = self.on_message
            self.client.subscribe('/devices/{}/events/commands'.format(
                GCLOUD_CONFIG['device_id'], 1))

            self.client.connect(
                args['mqtt_bridge_hostname'],
                args['mqtt_bridge_port'])

            self.client.loop_start()

        except Exception as e:
            print("Error connecting to GCloud:")
            print(e)

    def publish(self, topic, data):
        try:
            blob = json.dumps(data)
            # print('Publishing message: \'{}\''.format(blob))
            self.client.publish(self.mqtt_topic + '/' + topic, blob, qos=1)
        except Exception as e:
            print("Error publishing to GCloud:")
            print(e)

    def create_jwt(self, project_id, private_key_file, algorithm):
        token = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'aud': project_id
        }

        with open(private_key_file, 'r') as f:
            private_key = f.read()

        return jwt.encode(token, private_key, algorithm=algorithm)
