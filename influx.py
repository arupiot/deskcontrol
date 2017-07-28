from navigation import StateModule
from influxdb import InfluxDBClient
from datetime import datetime, timedelta


class InfluxModule(StateModule):
    name = "influx"
    controller = None
    client = None
    always_tick = True

    def __init__(self, controller):
        self.controller = controller
        super(InfluxModule, self).__init__(controller)

    def connect(self, auth):
        if auth:
            self.client = InfluxDBClient(
                auth["host"],
                auth["port"],
                auth["user"],
                auth["pass"],
                auth["db"],)
                # ssl=True, verify_ssl=False, timeout=2.0,)
        if self.client:
            print("InfluxDB connection: ", self.client)
        # if self.client:
        #    self.client.create_database(auth["db"])

    def push_value(self, key, value, tags={}):
        if self.client:

            ident = self.controller.modules["IdentityModule"].get_ident()
            data = [{
                "measurement": str(ident + "_" + key),
                "time":
                    datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
                "tags": tags,
                "fields": {"value": value, }
            }]
# {
#         "measurement": "cpu_load_short",
#         "tags": {
#             "host": "server01",
#             "region": "us-west"
#         },
#         "time": "2009-11-10T23:00:00Z",
#         "fields": {
#             "value": 0.64
#         }
#     }
# {'fields': {'value': 35},
#  'time': '2017-07-28T23:10:42Z',
#  'tags': {'type': 'light'},
#  'measurement': 'XXXX_LightingSystem_Luminance_Sensor'}

            print(data)
            self.client.write_points(data)

    def add_sensor(self, sensor):
        # Callbacks not implemented because TF callbacks are terrible
        pass

    def tick(self):
        if self.client and "SensorModule" in self.controller.modules:
            for key in self.controller.modules["SensorModule"].sensors:
                sensor = self.controller.modules["SensorModule"].sensors[key]
                update = False
                if "updated" not in sensor:
                    update = True
                elif sensor["updated"] < (datetime.now() -
                                          timedelta(minutes=1)):
                    update = True
                if update:
                    sensor["updated"] = datetime.now()
                    self.controller.modules["SensorModule"].update_sensor(
                        sensor)
                    self.push_value(
                        str(sensor["brick"]),
                        sensor["value"],
                        {"type": sensor["type"], })
