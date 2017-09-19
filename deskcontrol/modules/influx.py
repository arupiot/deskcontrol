from navigation import StateModule
from influxdb import InfluxDBClient
from config import INFLUX_AUTH


class InfluxModule(StateModule):
    client = None

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

    def publish(self, topic, data):
        try:
            if topic == "sensors":
                self.client.write_points([data])
        except Exception as e:
            print("Error publishing to InfluxDB:")
            print(e)
