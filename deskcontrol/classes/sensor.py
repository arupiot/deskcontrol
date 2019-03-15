from datetime import datetime
from helpers import seconds_past

class Sensor():
    def __init__(self, uid, sensor_config):
        self.sensor_config = {
            "name": "Temperature",
            "units": "C",
            "brick_tag": "Temperature_Sensor",
            "multiplier": 0.01,
            "variance": 1,
        }
        self.instance = self.sensor["class"](self.raw_uid, controller.ipcon)
        self.update_time = 300
        self.publish_limit = 20
        self.variance = 5
        self.change_callbacks = []
        self.published_value = None
        for attr in [
                "brick_tag", "value_func", "units", "multiplier", "offset",
                "update_time", "publish_limit", "variance", "sequence"]:
            if attr in self.sensor:
                setattr(self, attr, self.sensor[attr])             
        self.uid = str(self.raw_uid) + "_" + self.brick_tag + "_" + self.sensor_config["name"]
        # if "callback_func" in sensor:
        #    self.instance.register_callback(
        #        getattr(self.instance, sensor["callback_func"]),
        #        self.callback)
        self.value = None
        self.get_value()
        self.published = datetime.utcfromtimestamp(0)

    def parse_value(self, value):
        return value

    def get_value(self):
        try:
            self.instance = self.sensor["class"](self.raw_uid, self.controller.ipcon)
            if self.sensor_type == "magfield":
                value = getattr(self.instance, self.value_func)(False)
            else:
                value = getattr(self.instance, self.value_func)()
            value = self.parse_value(value)
            print(self.sensor_config["name"] + ': ' + str(value) + self.sensor["units"])
            self.updated = datetime.now()
            self.value = value
            return self.value
        except Exception as e:
            print("Error reading value from sensor:", e)
            pass

    def publish(self):
        if self.value and seconds_past(self.published, self.publish_limit):
            self.published_value = self.value
            self.published = datetime.now()
            self.controller.event("sensor-publish", self)

    def roc(self):
        if seconds_past(self.published, self.publish_limit):
            if not self.published_value:
                self.published_value = self.value
            self.get_value()
            if self.value:
                try:
                    for callback in self.change_callbacks:
                        callback(self.value)
                    if (self.value <= self.published_value - self.variance or
                        self.value >= self.published_value + self.variance):
                        self.publish()
                    if seconds_past(self.published, self.update_time):
                        self.publish()
                except Exception as e:
                    print("Error publishing value from sensor:", e)

    def get_value_display(self):
        if not self.value:
            return "None"
        if self.sensor_type == "motion" or self.sensor_type == "IMU_leds":
            if self.value == 1:
                return "Yes"
            else:
                return "No"
        return str(self.value) + " " + self.units

    def __str__(self):
        return self.uid
