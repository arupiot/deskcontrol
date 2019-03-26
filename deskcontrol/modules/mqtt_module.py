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
import json
import paho.mqtt.client as mqtt
from config import *



class MQTTModule(StateModule):
    client = None

    def __init__(self, controller):
        super(MQTTModule, self).__init__(controller)
        controller.add_event_handler("sensor-publish", self.publish_sensor)
        controller.add_event_handler("kiln-publish", self.publish_kiln)
        self.mqtt_topic = self.publish_topic
        self.connect()

    # a set of properties that are overridden in the google iot version

    @property
    def publish_topic(self):
        return MQTT_CONFIG['mqtt_publish_topic']

    @property
    def subscribe_topic(self):
        return MQTT_CONFIG['mqtt_subscribe_topic']

    @property
    def client_id(self):
        return MQTT_CONFIG['mqtt_client_id']

    @property
    def password(self):
        return MQTT_CONFIG['mqtt_password']

    @property
    def username(self):
        return MQTT_CONFIG['mqtt_username']

    @property
    def mqtt_host_name(self):
        return MQTT_CONFIG['mqtt_broker_host']

    @property
    def mqtt_port(self):
        return MQTT_CONFIG['mqtt_broker_port']

    def set_tls(self, client):
        pass


    def on_message(self, userdata, message):
        print(userdata, message)

    def connect(self):
        try:
            self.client = mqtt.Client(client_id=self.client_id)

            if self.username is not None:
                self.client.username_pw_set(
                    username=self.username,
                    password=self.password
                )

            self.set_tls(self.client)

            self.client.on_message = self.on_message
            self.client.subscribe(self.subscribe_topic)

            self.client.connect(
                self.mqtt_host_name,
                self.mqtt_port)

            self.client.loop_start()

        except Exception as e:
            print("Error connecting to MQTT:")
            print(e)

    def publish_sensor(self, data):

        data = {
            "measurement": data.brick_tag,
            "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "tags": {
                "sensor_type": data.brick_tag,
                "device_name": DEVICE_NAME,
                "name_authority": NAME_AUTHORITY
             },
            data.uid: data.value,
        }

        try:
            blob = json.dumps(data)
            result = self.client.publish(self.mqtt_topic + '/sensor', blob, qos=0)
            print("trying to MQTT")
            result.wait_for_publish()
            print("published to MQTT", blob)
        except Exception as e:
            print("Error publishing to MQTT:")
            print(e)

    def publish_kiln(self, data):
        try:
            blob = json.dumps(data)
            self.client.publish(self.mqtt_topic + '/kiln', blob, qos=1)
            # print("published to googleiot", blob)
        except Exception as e:
            print("Error publishing to MQTT:")
            print(e)
