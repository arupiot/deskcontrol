from classes.tfmodule import TinkerForgeModule
from classes.tfsensor import TinkerforgeSensor
import logging


class TinkerforgeSensorModule(TinkerForgeModule):
    menu_title = "Sensors"
    sensors = {}
    current = 0

    def __init__(self, *args, **kwargs):
        super(TinkerforgeSensorModule, self).__init__(*args, **kwargs)
        self.add_to_menu("Sensors")

    def draw(self):
        if not len(self.sensors):
            self.push({"type": "render_data", "data": {}})
            return
        sensor = self.sensors[list(self.sensors.keys())[self.current]]
        sensor.get_value()
        name = sensor.name
        self.push({"type": "render_data", "data": {
            "values",
            {"title": name,
             "value": sensor.value, }}})

    def try_bricklet(self, uid, device_identifier, position):
        sensors = []
        if device_identifier == 216:
            sensors.append(TinkerforgeSensor(
                uid, "temp", self.ipcon))
        elif device_identifier == 217:
            sensors.append(TinkerforgeSensor(
                uid, "ir_temp", self.ipcon))
        elif device_identifier == 27:
            sensors.append(TinkerforgeSensor(
                uid, "humidity", self.ipcon))
        elif device_identifier == 259:
            sensors.append(TinkerforgeSensor(
                uid, "light", self.ipcon))
        elif device_identifier == 238:
            sensors.append(TinkerforgeSensor(
                uid, "sound", self.ipcon))
        elif device_identifier == 262:
            sensors.append(TinkerforgeSensor(
                uid, "co2", self.ipcon))
        elif device_identifier == 227:
            sensors.append(TinkerforgeSensor(
                uid, "voltage", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "current", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "power", self.ipcon))
        elif device_identifier == 25:
            sensors.append(TinkerforgeSensor(
                uid, "dist", self.ipcon))
        elif device_identifier == 243:
            sensors.append(TinkerforgeSensor(
                uid, "colour", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "colour_temp", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "colour_illuminance", self.ipcon))
        elif device_identifier == 221:
            sensors.append(TinkerforgeSensor(
                uid, "air_pressure", self.ipcon))
        elif device_identifier == 241:
            sensors.append(TinkerforgeSensor(
                uid, "reflectivity", self.ipcon))
        elif device_identifier == 240:
            sensors.append(TinkerforgeSensor(
                uid, "magfield", self.ipcon))
        elif device_identifier == 250:
            sensors.append(TinkerforgeSensor(
                uid,"acceleration_xyz", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "acceleration_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "acceleration_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "acceleration_Z", self.ipcon))
        elif device_identifier == 232:
            sensors.append(TinkerforgeSensor(
                uid, "moisture", self.ipcon))
        elif device_identifier == 265:
            sensors.append(TinkerforgeSensor(
                uid, "uv", self.ipcon))
        elif device_identifier == 26:
            sensors.append(TinkerforgeSensor(
                uid, "dual_relay", self.ipcon))
        elif device_identifier == 233:
            sensors.append(TinkerforgeSensor(
                uid, "motion", self.ipcon))
        elif device_identifier == 230:
            sensors.append(TinkerforgeSensor(
                uid, "dual_button_state", self.ipcon))
        elif device_identifier == 282:
            sensors.append(TinkerforgeSensor(
                uid, "rgb_led_button_colour", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "rgb_led_button_state", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "rgb_led_button_colour_r", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "rgb_led_button_colour_g", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "rgb_led_button_colour_b", self.ipcon))
        elif device_identifier == 292:
            sensors.append(TinkerforgeSensor(
                uid, "motion_2", self.ipcon))
        elif device_identifier == 215:
            sensors.append(TinkerforgeSensor(
                uid, "rotation_poti", self.ipcon))
        elif device_identifier == 239:
            sensors.append(TinkerforgeSensor(
                uid, "tilt", self.ipcon))
        elif device_identifier == 229:
            sensors.append(TinkerforgeSensor(
                uid, "dist_us", self.ipcon))
        elif device_identifier == 294:
            sensors.append(TinkerforgeSensor(
                uid, "rotation_encoder_2", self.ipcon))
        elif device_identifier == 213:
            sensors.append(TinkerforgeSensor(
                uid, "linear_poti", self.ipcon))
        elif device_identifier == 278:
            sensors.append(TinkerforgeSensor(
                uid, "thermal_image", self.ipcon))
        elif device_identifier == 241:
            sensors.append(TinkerforgeSensor(
                uid, "reflectivity", self.ipcon))
        elif device_identifier == 283:
            sensors.append(TinkerforgeSensor(
                uid, "humidity_temp", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "humidity_v2", self.ipcon))
        elif device_identifier == 18:
            sensors.append(TinkerforgeSensor(
                uid, "heading", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "roll", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "pitch", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "linear_acceleration_Z", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "linear_acceleration_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "linear_acceleration_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "gravity_acceleration_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "gravity_acceleration_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "gravity_acceleration_Z", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "IMU_leds", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "IMU_acceleration_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "IMU_acceleration_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "IMU_acceleration_Z", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "angular_velocity_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "angular_velocity_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "angular_velocity_Z", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "linear_acceleration_xyz", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "gravity_acceleration_xyz", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "IMU_acceleration_xyz", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "angular_velocity_xyz", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "quaternion_W", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "quaternion_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "quaternion_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "quaternion_Z", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "IMU_temp", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "magnetic_field_X", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "magnetic_field_Y", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "magnetic_field_Z", self.ipcon))
            sensors.append(TinkerforgeSensor(
                uid, "magnetic_field_xyz", self.ipcon))
        for sensor in sensors:
            sensor.register_callback(self.push)
            self.sensors[sensor.sensor_type + "_" + uid] = sensor
	
    def callback_request_sensor_metadata(self, data):
        self.push({"type": "sensor_metadata", "data": self.sensors})

    def callback_input(self, data):
        direction = data["data"]
        if direction in ["back", "left"]:
            self.push({"type": "input", "switch": "MenuModule"})
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.sensors):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.sensors) - 1
            self.draw()

    def tick(self):
        for pk in self.sensors:
            self.sensors[pk].roc()
            logging.debug("sensor tick")
        self.wait(1)
