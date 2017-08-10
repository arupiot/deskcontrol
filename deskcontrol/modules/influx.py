from navigation import StateModule
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from config import INFLUX_AUTH


class InfluxModule(StateModule):
    client = None
    always_tick = True

    def __init__(self, controller):
        super(InfluxModule, self).__init__(controller)
        controller.publishers.append(self.publish)
        self.connect(INFLUX_AUTH)

    def connect(self, auth):
        try:
            self.client = InfluxDBClient(
                auth["host"], auth["port"], auth["user"], auth["pass"],
                auth["db"],)
        except Exception as e:
            print("Error connecting to InfluxDB:")
            print(e)

    def publish(self, controller, key, value, tags={}):
        try:
            ident = self.controller.identity
            if self.client:
                data = [{
                    "measurement": str(ident + "_" + key),
                    "time": (
                        datetime.utcnow().replace(microsecond=0).isoformat() +
                        "Z"),
                    "tags": tags,
                    "fields": {"value": value, }
                }]
            self.client.write_points(data)
            print("published %s" % str(ident + "_" + key))
        except Exception as e:
            print("Error publishing to InfluxDB:")
            print(e)

    def tick(self):
        if self.client and "SensorModule" in self.controller.modules:
            for key in self.controller.modules["SensorModule"].sensors:
                sensor = self.controller.modules["SensorModule"].sensors[key]
                if sensor.updated < (datetime.now() -
                                     timedelta(minutes=1)):
                    sensor.get_value()
