from navigation import StateModule
from config import *
import json
import requests


class HttpPushModule(StateModule):
    client = None

    def __init__(self, controller):
        super(HttpPushModule, self).__init__(controller)
        controller.add_event_handler("kiln-publish", self.publish_kiln)

    def publish_kiln(self, data):
        try:
            blob = json.dumps(data)
            requests.post(
                SCHEMA_POST_URL,
                data=blob,
                timeout=0.5)
            print("pushed to HTTP", blob)
        except Exception as e:
            print("Error pushing via HTTP:")
            print(e)
