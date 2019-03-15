from iotnode.module import NodeModule
import json
import requests
import logging


class HttpPushModule(NodeModule):
    def callback_kiln_publish(self, data):
        try:
            blob = json.dumps(data)
            requests.post(
                self.cache['SCHEMA_POST_URL'],
                data=blob,
                timeout=0.5)
            logging.debug("Pushed to HTTP", blob)
        except Exception as e:
            logging.error("Error pushing via HTTP: " + str(e))
