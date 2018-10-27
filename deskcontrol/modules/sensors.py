from datetime import datetime
from modules.navigation import StateModule
from modules.sensor_types import SENSORS
import numbers
from helpers import seconds_past
import math


class Sensor():
    def __init__(self, controller, sensor_type, uid):
        if sensor_type not in SENSORS:
            raise Exception
        self.raw_uid = uid
        self.sensor = SENSORS[sensor_type]
        self.name = self.sensor["name"]
        self.sensor_type = sensor_type
        self.controller = controller
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
        self.uid = str(self.raw_uid) + "_" + self.brick_tag + "_" + self.name
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
            print(self.name + ': ' + str(value) + self.sensor["units"])
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
                for callback in self.change_callbacks:
                        callback(self.value)
                if (self.value <= self.published_value - self.variance or
                        self.value >= self.published_value + self.variance):
                    self.publish()
                if seconds_past(self.published, self.update_time):
                    self.publish()

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


class SensorModule(StateModule):
    menu_title = "Sensors"
    sensors = {}
    current = 0

    def __init__(self, controller):
        super(SensorModule, self).__init__(controller)
        self.update_sensors()
        controller.add_event_handler("sensor-created", self.force_update)

    def draw(self, clear=True):
        if self.controller.screen and self.controller.current_module == self:
            if clear:
                self.controller.screen.device.clear_display()
            if not len(self.sensors):
                self.controller.screen.draw("values", {})
                return
            sensor = self.sensors[list(self.sensors.keys())[self.current]]
            sensor.get_value()
            unique_name = None
            if self.controller.localdb:
                unique_name = self.controller.localdb.get(sensor.uid)
            if unique_name:
                name = unique_name
            else:
                name = sensor.name
            self.controller.screen.draw(
                "values",
                {"title": name,
                 "value": str(sensor.get_value_display())})

    def try_bricklet(self, uid, device_identifier, position):
        sensors = []
        if device_identifier == 216:
            sensors.append(Sensor(self.controller, "temp", uid))
        elif device_identifier == 217:
            sensors.append(Sensor(self.controller, "ir_temp", uid))
        elif device_identifier == 27:
            sensors.append(Sensor(self.controller, "humidity", uid))
        elif device_identifier == 259:
            sensors.append(Sensor(self.controller, "light", uid))
        elif device_identifier == 238:
            sensors.append(Sensor(self.controller, "sound", uid))
        elif device_identifier == 262:
            sensors.append(Sensor(self.controller, "co2", uid))
        elif device_identifier == 227:
            sensors.append(Sensor(self.controller, "voltage", uid))
            sensors.append(Sensor(self.controller, "current", uid))
            sensors.append(Sensor(self.controller, "power", uid))
        elif device_identifier == 25:
            sensors.append(Sensor(self.controller, "dist", uid))
        elif device_identifier == 243:
            sensors.append(Sensor(self.controller, "colour", uid))
            sensors.append(Sensor(self.controller, "colour_temp", uid))
            sensors.append(Sensor(self.controller, "colour_illuminance", uid))
        elif device_identifier == 221:
            sensors.append(Sensor(self.controller, "air_pressure", uid))
        elif device_identifier == 241:
            sensors.append(Sensor(self.controller, "reflectivity", uid))
        elif device_identifier == 240:
            sensors.append(Sensor(self.controller, "magfield", uid))
        elif device_identifier == 250:
            sensors.append(Sensor(self.controller,"acceleration_xyz", uid))
            sensors.append(Sensor(self.controller, "acceleration_X", uid))
            sensors.append(Sensor(self.controller, "acceleration_Y", uid))
            sensors.append(Sensor(self.controller, "acceleration_Z", uid))
        elif device_identifier == 232:
            sensors.append(Sensor(self.controller, "moisture", uid))
        elif device_identifier == 265:
            sensors.append(Sensor(self.controller, "uv", uid))
        elif device_identifier == 26:
            sensors.append(Sensor(self.controller, "dual_relay", uid))
        elif device_identifier == 233:
            sensors.append(Sensor(self.controller, "motion", uid))
        elif device_identifier == 230:
            sensors.append(Sensor(self.controller, "dual_button_state", uid))
        elif device_identifier == 282:
            sensors.append(Sensor(self.controller, "rgb_led_button_colour", uid))
            sensors.append(Sensor(self.controller, "rgb_led_button_state", uid))
            sensors.append(Sensor(self.controller, "rgb_led_button_colour_r", uid))
            sensors.append(Sensor(self.controller, "rgb_led_button_colour_g", uid))
            sensors.append(Sensor(self.controller, "rgb_led_button_colour_b", uid))
        elif device_identifier == 292:
            sensors.append(Sensor(self.controller, "motion_2", uid))
        elif device_identifier == 215:
            sensors.append(Sensor(self.controller, "rotation_poti", uid))
        elif device_identifier == 239:
            sensors.append(Sensor(self.controller, "tilt", uid))
        elif device_identifier == 229:
            sensors.append(Sensor(self.controller, "dist_us", uid))
        elif device_identifier == 294:
            sensors.append(Sensor(self.controller, "rotation_encoder_2", uid))
        elif device_identifier == 213:
            sensors.append(Sensor(self.controller, "linear_poti", uid))
        elif device_identifier == 278:
            sensors.append(Sensor(self.controller, "thermal_image", uid))
        elif device_identifier == 241:
            sensors.append(Sensor(self.controller, "reflectivity", uid))
        elif device_identifier == 283:
            sensors.append(Sensor(self.controller, "humidity_temp", uid))
            sensors.append(Sensor(self.controller, "humidity_v2", uid))
        elif device_identifier == 18:
            sensors.append(Sensor(self.controller, "heading", uid))
            sensors.append(Sensor(self.controller, "roll", uid))
            sensors.append(Sensor(self.controller, "pitch", uid))
            sensors.append(Sensor(self.controller, "linear_acceleration_Z", uid))
            sensors.append(Sensor(self.controller, "linear_acceleration_Y", uid))
            sensors.append(Sensor(self.controller, "linear_acceleration_X", uid))
            sensors.append(Sensor(self.controller, "gravity_acceleration_X", uid))
            sensors.append(Sensor(self.controller, "gravity_acceleration_Y", uid))
            sensors.append(Sensor(self.controller, "gravity_acceleration_Z", uid))
            sensors.append(Sensor(self.controller, "IMU_leds", uid))
            sensors.append(Sensor(self.controller, "IMU_acceleration_Y", uid))
            sensors.append(Sensor(self.controller, "IMU_acceleration_X", uid))
            sensors.append(Sensor(self.controller, "IMU_acceleration_Z", uid))
            sensors.append(Sensor(self.controller, "angular_velocity_X", uid))
            sensors.append(Sensor(self.controller, "angular_velocity_Y", uid))
            sensors.append(Sensor(self.controller, "angular_velocity_Z", uid))
            sensors.append(Sensor(self.controller, "linear_acceleration_xyz", uid))
            sensors.append(Sensor(self.controller, "gravity_acceleration_xyz", uid))
            sensors.append(Sensor(self.controller, "IMU_acceleration_xyz", uid))
            sensors.append(Sensor(self.controller, "angular_velocity_xyz", uid))
            sensors.append(Sensor(self.controller, "quaternion_W", uid))
            sensors.append(Sensor(self.controller, "quaternion_X", uid))
            sensors.append(Sensor(self.controller, "quaternion_Y", uid))
            sensors.append(Sensor(self.controller, "quaternion_Z", uid))
            sensors.append(Sensor(self.controller, "IMU_temp", uid))
            sensors.append(Sensor(self.controller, "magnetic_field_X", uid))
            sensors.append(Sensor(self.controller, "magnetic_field_Y", uid))
            sensors.append(Sensor(self.controller, "magnetic_field_Z", uid))
            sensors.append(Sensor(self.controller, "magnetic_field_xyz", uid))
        for sensor in sensors:
            self.sensors[sensor.sensor_type + "_" + uid] = sensor	
            self.controller.event("sensor-created", sensor)
	
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

    def update_sensors(self):
        for pk in self.sensors:
            self.sensors[pk].roc()
        self.controller.scheduler.enter(1, 1, self.update_sensors, (),)

    def tick(self):
        self.draw(clear=False)

    def force_update(self, sensor):
        sensor.publish()
