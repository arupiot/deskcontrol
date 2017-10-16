from navigation import StateModule
from influxdb import InfluxDBClient
from config import INFLUX_AUTH
from helpers import sensor_data


class InfluxModule(StateModule):
    client = None

    def __init__(self, controller):
        super(InfluxModule, self).__init__(controller)
        controller.add_event_handler("sensor-publish", self.publish_sensor)
        self.connect(INFLUX_AUTH)

    def connect(self, auth):
        try:
            self.client = InfluxDBClient(
                auth["host"], auth["port"], auth["user"], auth["pass"],
                auth["db"], auth["ssl"])
        except Exception as e:
            print("Error connecting to InfluxDB:")
            print(e)

    def publish_sensor(self, data):
        try:
            data = sensor_data(
                self.controller,
                data.uid,
                str(data.value),
                {"type": data.brick_tag, }, )
            self.client.write_points([data])
            print("published to influx", data)
        except Exception as e:
            print("Error publishing to InfluxDB:")
            print(e)
