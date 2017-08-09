from navigation import StateModule
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from config import INFLUX_AUTH


class InfluxModule(StateModule):
    name = "influx"
    controller = None
    client = None
    always_tick = True

    def __init__(self, controller):
        self.controller = controller
        super(InfluxModule, self).__init__(controller)
        controller.publishers.append(self.publish)
        self.connect(INFLUX_AUTH)

    def connect(self, auth):
        if auth:
            self.client = InfluxDBClient(
                auth["host"], auth["port"], auth["user"], auth["pass"],
                auth["db"],)

    def publish(self, key, value, tags={}):
        try:
            if self.client:
                ident = self.controller.modules["IdentityModule"].get_ident()
                data = [{
                    "measurement": str(ident + "_" + key),
                    "time": (
                        datetime.utcnow().replace(microsecond=0).isoformat() +
                        "Z"),
                    "tags": tags,
                    "fields": {"value": value, }
                }]
            self.client.write_points(data)
        except Exception as e:
            print(e)

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
                    self.publish(
                        str(sensor["brick"]),
                        sensor["value"],
                        {"type": sensor["type"], })
