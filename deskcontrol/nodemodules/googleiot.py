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

from iotnode.module import NodeModule
from datetime import datetime, timedelta
import jwt
import logging
import json
import paho.mqtt.client as mqtt
from helpers import sensor_data_format


class GoogleIoTModule(NodeModule):
    client = None

    def __init__(self, *args, **kwargs):
        super(GoogleIoTModule, self).__init__(*args, **kwargs)
        self.mqtt_topic = '/devices/{}/events'.format(
            self.cache['_GCLOUD_CONFIG']['device_id'])
        self.connect()

    def on_message(self, userdata, message):
        logging.info("MQTT Message: ",userdata, message)

    def connect(self):
        try:
            args = self.cache['_GCLOUD_CONFIG']
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
                args['device_id'], 1))

            self.client.connect(
                args['mqtt_bridge_hostname'],
                args['mqtt_bridge_port'])

            self.client.loop_start()

        except Exception as e:
            logging.error("Error connecting to GCloud: " + str(e))

    def callback_sensor_publish(self, data):
        data = sensor_data_format(
            self.cache['IDENT_SHORT'],
            data.uid,
            str(data.value),
            {"type": data.brick_tag, }, )
        try:
            blob = json.dumps(data)
            self.client.publish(self.mqtt_topic + '/sensor', blob, qos=1)
        except Exception as e:
            logging.error("Error publishing to GCloud: " + str(e))

    def callback_kiln_publish(self, data):
        try:
            blob = json.dumps(data)
            self.client.publish(self.mqtt_topic + '/kiln', blob, qos=1)
        except Exception as e:
            logging.error("Error publishing to GCloud: " + str(e))

    def create_jwt(self, project_id, private_key_file, algorithm):
        token = {
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=60),
            'aud': project_id
        }

        with open(private_key_file, 'r') as f:
            private_key = f.read()

        return jwt.encode(token, private_key, algorithm=algorithm)
