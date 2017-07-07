from navigation import StateModule
from urlparse import urlparse
import urllib
import json
import requests
import os
from helpers.rsa import generateNewRandomAlphaNumeric, sign_url
from config import CREDS_PATH, CREDS_PREFIX, SHORT_IDENT, INFLUX_AUTH


class IdentityModule(StateModule):
    name = "identity"
    controller = None
    ident = None

    def __init__(self, controller):
        self.controller = controller
        super(IdentityModule, self).__init__(controller)
        self.get_ident()
        # print(get_config())

        # Influx Auth should come from identify system, not config
        # Currently relys on order of modules being loaded to be correct...
        if "InfluxModule" in self.controller.modules:
            self.controller.modules["InfluxModule"].connect(INFLUX_AUTH)

    def get_ident(self):
        self.ident = SHORT_IDENT

    def get_config(self):
        # TO BE FIXED
        creds_path = None

        for filename in os.listdir(CREDS_PATH):
            if filename.startswith(CREDS_PREFIX):
                creds_path = os.path.join(CREDS_PATH, filename)

        with open(creds_path, "r") as f:
            creds = json.loads(f.read())

        cpu_serial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpu_serial = line[10:26]
                    f.close()
        except Exception:
            cpu_serial = "ERROR000000000"

        src_url = creds["url"]
        private_pem = creds["private_key"]
        parsed = urlparse(src_url)
        nonced_path = "%s/%s" % (
            parsed.path, generateNewRandomAlphaNumeric(20))
        sig = sign_url(nonced_path, private_pem)
        query = urllib.urlencode({"sig": sig, "serial": cpu_serial})
        url = "%s://%s%s?%s" % (
            parsed.scheme, parsed.netloc, nonced_path, query)

        rsp = requests.get(url)

        if rsp.status_code == 200:
            return rsp.json()

        if rsp.status_code == 409:
            print("Error: another device is using this key already")

        return None
