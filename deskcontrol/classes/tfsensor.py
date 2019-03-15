from classes import Sensor
from datetime import datetime
import numbers
from helpers import seconds_past
import math
from classes.tftypes import SENSORS


class TinkerforgeSensor(Sensor):
    def __init__(self, uid, sensor_type, connection):
        if sensor_type not in SENSORS:
            raise Exception
        self.raw_uid = uid
        self.sensor_config = SENSORS[sensor_type]
        self.sensor_type = sensor_type
        self.instance = self.sensor["class"](self.raw_uid, connection)
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
        if self.sensor_type == "dualrelay":
            value = str(value[0]) + str(value[1])
        elif self.sensor_type == "acceleration_X":
            value = value[0]
        elif self.sensor_type == "acceleration_Y":
            value = value[1]
        elif self.sensor_type == "acceleration_Z":
            value = value[2]
        elif self.sensor_type == "colour":
            r, g, b, c = [int(x / 257) for x in value]
            print(r, g, b, c)
        elif self.sensor_type == "rgb_led_button_colour":
            r,g,b = [int(x) for x in value]
            value = (r+g+b)/3
        elif self.sensor_type == "rgb_led_button_colour_r":
            value = value[0]
        elif self.sensor_type == "rgb_led_button_colour_g":
            value = value[1]
        elif self.sensor_type == "rgb_led_button_colour_b":
            value = value[2]
        elif self.sensor_type == "heading":
            value = value[0]
        elif self.sensor_type == "roll":
            value = value[1]
        elif self.sensor_type == "pitch":
            value = value[2]
        elif self.sensor_type[-4:].lower() == "_xyz":
            x,y,z = [int(x) for x in value]
            value = math.sqrt(x**2+y**2+z**2)
        elif self.sensor_type == "quaternion_W":
            value = value[0]
        elif self.sensor_type[-2:].upper() == "_X":
            if "quaternion" in self.sensor_type:
                value = value[1]
            else:
                value = value[0]
        elif self.sensor_type[-2:].upper() == "_Y":
            if "quaternion" in self.sensor_type:
                value = value[2]
            else:
                value = value[1]
        elif self.sensor_type[-2:].upper() == "_Z":
            if "quaternion" in self.sensor_type:
                value = value[3]
            else:
                value = value[2]
        elif isinstance(value,bool):
            if value:
                value = 1
            else:
                value = 0
        if isinstance(value, numbers.Number):
            if hasattr(self, "multiplier"):
                value = value * self.multiplier
            if hasattr(self, "offset"):
                value = value + self.offset
        return value

    def callback(sel, value=None):
        self.value = self.parse_value(value)
        self.updated = datetime.now()
        self.publish()

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
