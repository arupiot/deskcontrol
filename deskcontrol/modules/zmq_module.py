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
import zmq
from config import *
from helpers import mqtt_sensor_data


class ZMQModule(StateModule):
    socket = None

    def __init__(self, controller):
        super(ZMQModule, self).__init__(controller)
        controller.add_event_handler("sensor-publish", self.publish_sensor)
        self.topic = ZMQ_CONFIG["zmq_topic"]
        self.connect()


    def connect(self):

        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % ZMQ_CONFIG["zmq_port"])


    def publish_sensor(self, data):
        data = mqtt_sensor_data(
            self.controller,
            data.uid,
            data.value,
            {
                "sensor_type": data.brick_tag,
                "device_name": DEVICE_NAME,
                "name_authority": NAME_AUTHORITY
             },
        )
        try:
            blob = json.dumps(data)
            self.socket.send("%s %s" % (self.topic + '/sensor', blob))
            print("published to ZMQ")
        except Exception as e:
            print("Error publishing to ZMQ:")
            print(e)
