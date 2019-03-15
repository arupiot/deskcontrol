#!/usr/bin/env python
#  Arup IoT Desk Controller
#  Ben Hussey <ben.hussey@arup.com> - March 2019

from iotnode.controller import Controller
from config import *


class DeskController(Controller):
    def __init__(self, *args, **kwargs):
        for var in ['TINKERFORGE', 'SHORT_IDENT',
                    'INFLUX_AUTH', 'GCLOUD_CONFIG']:
            self.cache['_' + var] = globals()[var]

        super(DeskController, self).__init__(*args, **kwargs)

if __name__ == "__main__":
    node = DeskController(MODULES)
    node.start()
