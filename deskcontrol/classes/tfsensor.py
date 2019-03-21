from classes.sensor import Sensor
from datetime import datetime
import numbers
import math
import logging
from classes.tftypes import SENSORS


class TinkerforgeSensor(Sensor):
    def __init__(self, uid, sensor_type, ipcon, **kwargs):
        if sensor_type not in SENSORS:
            logging.error("Sensor type not found")
            exit()
        
        self.sensor_type = sensor_type
        self.sensor_config = SENSORS[sensor_type]
        self.ipcon = ipcon

        super(TinkerforgeSensor, self).__init__(uid, self.sensor_config)

        self.instance = self.sensor_config["class"](self.raw_uid, ipcon)

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

    def callback(self, value=None):
        self.value = self.parse_value(value)
        self.updated = datetime.now()
        self.publish()

    def get_value(self):
        try:
            self.instance = self.sensor_config["class"](self.raw_uid, self.ipcon)
            if self.sensor_type == "magfield":
                value = getattr(self.instance, self.value_func)(False)
            else:
                value = getattr(self.instance, self.value_func)()
            value = self.parse_value(value)
            self.updated = datetime.now()
            self.value = value
            return self.value
        except Exception as e:
            logging.error("Error reading value from sensor:" + str(e))

    def get_value_display(self):
        if self.sensor_type == "motion" or self.sensor_type == "IMU_leds":
            if self.value == 1:
                return "Yes"
            else:
                return "No"
        return super(TinkerforgeSensor, self).get_value_display()
