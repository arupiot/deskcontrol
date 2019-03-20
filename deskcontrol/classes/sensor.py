from datetime import datetime
from helpers import seconds_past
import logging


class Sensor():
    update_time = 300
    publish_limit = 20
    variance = 5
    published_value = None
    value = None
    publish_callback = None

    def __init__(self, uid, sensor_config):
        # self.sensor_config = {
        #     "name": "Temperature",
        #     "units": "C",
        #     "brick_tag": "Temperature_Sensor",
        #     "multiplier": 0.01,
        #     "variance": 1,
        # }
        self.raw_uid = uid
        for attr in [
                "brick_tag", "value_func", "units", "multiplier", "offset",
                "update_time", "publish_limit", "variance", "sequence"]:
            if attr in sensor_config:
                setattr(self, attr, sensor_config[attr])
        self.uid = (str(self.raw_uid) + "_" + self.brick_tag + "_" + 
                    self.sensor_config["name"])
        self.get_value()
        self.published = datetime.utcfromtimestamp(0)

    def parse_value(self, value):
        return value

    def get_value(self):
        return None

    def register_callback(self, callback):
        self.publish_callback = callable

    def publish(self):
        if self.value and seconds_past(self.published, self.publish_limit):
            self.published_value = self.value
            self.published = datetime.now()
            if callable(self.publish_callback):
                self.publish_callback(
                    {"type": "sensor_publish", "data": self,})

    def roc(self):
        if seconds_past(self.published, self.publish_limit):
            if not self.published_value:
                self.published_value = self.value
            self.get_value()
            if self.value:
                try:
                    if (self.value <= self.published_value - self.variance or
                        self.value >= self.published_value + self.variance):
                        self.publish()
                    if seconds_past(self.published, self.update_time):
                        self.publish()
                except Exception as e:
                    logging.error(
                        "Error publishing value from sensor:" + str(e))

    def get_value_display(self):
        if not self.value:
            return "None"
        return str(self.value) + " " + self.units

    def __str__(self):
        return self.uid
