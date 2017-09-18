from datetime import datetime, timedelta
from navigation import StateModule
from sensor_types import SENSORS
import numbers
from helpers import sensor_data


class Sensor():
    def __init__(self, controller, sensor_type, uid):
        if sensor_type not in SENSORS:
            raise Exception
        sensor = SENSORS[sensor_type]
        self.name = sensor["name"]
        self.sensor_type = sensor_type
        self.controller = controller
        self.instance = sensor["class"](uid, controller.ipcon)
        self.update_time = 300
        self.change_limit = 5
        self.variance = 1
        for attr in [
                "brick_tag", "value_func", "units", "multiplier", "offset",
                "update_time", "change_limit", "variance"]:
            if attr in sensor:
                setattr(self, attr, sensor[attr])
        self.uid = str(uid) + "_" + self.brick_tag
        if "callback_func" in sensor:
            self.instance.register_callback(
                getattr(self.instance, sensor["callback_func"]),
                self.callback)
        self.get_value()
        self.published = datetime.utcfromtimestamp(0)
        self.publish()

    def parse_value(self, value):
        if self.sensor_type == "relay_a":
            value = value[0]
        elif self.sensor_type == "relay_b":
            value = value[1]
        elif self.sensor_type == "acceleration_x":
            value = value[0]
        elif self.sensor_type == "acceleration_y":
            value = value[1]
        elif self.sensor_type == "acceleration_z":
            value = value[2]
        elif self.sensor_type == "acceleration":
            x, y, z = value
        elif self.sensor_type == "colour":
            r, g, b, c = [int(x / 257) for x in value]
            print(r, g, b, c)

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
        if self.sensor_type == "magfield":
            value = getattr(self.instance, self.value_func)(False)
        else:
            value = getattr(self.instance, self.value_func)()

        value = self.parse_value(value)

        self.updated = datetime.now()
        self.value = value
        return self.value

    def publish(self):
        if (self.published < datetime.now() -
                timedelta(seconds=self.change_limit)):
            self.published_value = self.value
            self.published = datetime.now()
            self.controller.publish(
                "sensors",
                sensor_data(self.controller,
                            self.uid,
                            str(self.value),
                            {"type": self.brick_tag, }, ))

    def roc(self):
        if (self.updated < datetime.now() -
                timedelta(seconds=self.change_limit)):
            if not self.published_value:
                self.published_value = self.value
            self.get_value()
            if (self.value <= self.published_value - self.variance or
                    self.value >= self.published_value + self.variance):
                self.publish()
            if (self.published < datetime.now() -
                    timedelta(seconds=self.update_time)):
                self.publish()

    def __str__(self):
        if not self.value:
            self.get_value()
        if not self.value:
            return "None"
        return str(self.value) + " " + self.units


class SensorModule(StateModule):
    menu_title = "Sensors"
    always_tick = True
    sensors = {}
    current = 0

    def draw(self, clear=True):
        if self.controller.screen and self.controller.current_module == self:
            if clear:
                self.controller.screen.device.clear_display()
            if not len(self.sensors):
                self.controller.ipcon.enumerate()
                self.controller.screen.draw("values", {})
                return
            sensor = self.sensors[self.sensors.keys()[self.current]]
            self.controller.screen.draw(
                "values",
                {"title": sensor.name,
                 "value": str(sensor)})

    def try_bricklet(self, uid, device_identifier, position):
        sensor = None
        if device_identifier == 216:
            sensor = Sensor(self.controller, "temp", uid)
        elif device_identifier == 217:
            sensor = Sensor(self.controller, "irtemp", uid)
        elif device_identifier == 27:
            sensor = Sensor(self.controller, "humidity", uid)
        elif device_identifier == 259:
            sensor = Sensor(self.controller, "light", uid)
        elif device_identifier == 238:
            sensor = Sensor(self.controller, "sound", uid)
        elif device_identifier == 262:
            sensor = Sensor(self.controller, "co2", uid)
        elif device_identifier == 227:
            sensor = Sensor(self.controller, "voltage", uid)
            sensor = Sensor(self.controller, "current", uid)
            sensor = Sensor(self.controller, "power", uid)
        elif device_identifier == 25:
            sensor = Sensor(self.controller, "dist", uid)
        elif device_identifier == 243:
            sensor = Sensor(self.controller, "colour", uid)
            sensor = Sensor(self.controller, "colour_temp", uid)
        elif device_identifier == 221:
            sensor = Sensor(self.controller, "air_pressure", uid)
        elif device_identifier == 241:
            sensor = Sensor(self.controller, "reflectivity", uid)
        elif device_identifier == 240:
            sensor = Sensor(self.controller, "magfield", uid)
        # elif device_identifier == 250:
        #     sensor = Sensor(self.controller,"acceleration", uid)
        #    sensor = Sensor(self.controller, "acceleration_x", uid)
        #    sensor = Sensor(self.controller, "acceleration_y", uid)
        #    sensor = Sensor(self.controller, "acceleration_z", uid)
        elif device_identifier == 232:
            sensor = Sensor(self.controller, "moisture", uid)

        if sensor:
            self.sensors[sensor.uid] = sensor
            if "BrickModule" in self.controller.modules:
                self.controller.modules["BrickModule"].add_sensor(sensor)

    def navigate(self, direction):
        if direction == "back":
            self.controller.prev_module()
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.sensors):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.sensors) - 1
            # print("Sensor: " + str(list(self.sensors)[self.current]))
            self.draw()

    def tick(self):
        for pk in self.sensors:
            self.sensors[pk].roc()
        self.draw(clear=False)
