from modules.navigation import StateModule
from influxdb import InfluxDBClient
from helpers import sensor_data
from config import *

class InfluxModule(StateModule):
    client = None

    def __init__(self, controller):
        super(InfluxModule, self).__init__(controller)
        self.connect(INFLUX_AUTH)
        controller.add_event_handler("sensor-publish", self.publish_sensor)

    def connect(self, auth):
        try:
            self.client = InfluxDBClient(
                host=auth["host"],
                port=auth["port"],
                username=auth["user"],
                password=auth["pass"],
                database=auth["db"],
                ssl=auth["ssl"],
                timeout=1,
                retries=5,)
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
            # print("published to influx", data)
        except Exception as e:
            print("Error publishing to InfluxDB:")
            print(e)
