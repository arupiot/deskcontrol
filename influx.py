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
        self.client = InfluxDBClient(
            auth["host"],
            auth["port"],
            auth["user"],
            auth["pass"],
            auth["db"])
        self.client.create_database(auth["db"])

    def push_value(self, key, value, tags={}):
        data = {
            "measurement": key,
            "time": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "tags": tags,
            "fields": {"value": value, }
        }
        self.client.write_points([data])

    def add_sensor(self, sensor):
        # Callbacks not implemented because TF callbacks are terrible
        pass

    def tick(self):
        if "SensorModule" in self.controller.modules:
            for sensor in self.controller.modules["SensorModule"].sensors:
                if (not sensor.updated or
                        sensor.updated < (
                            datetime.now() - timedelta(minutes=1))):
                    sensor.updated = datetime.now()
                    ident = self.controller.modules["IdentityModule"].ident
                    self.controller.modules["SensorModule"].update_sensor(
                        sensor)
                    self.push_value(
                        str(ident + "_" + sensor["type"]),
                        sensor["value"])
