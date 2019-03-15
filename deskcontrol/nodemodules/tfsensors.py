from iotnode.module import NodeModule
from classes.tfsensor import TinkerforgeSensor


class TinkerforgeSensorModule(NodeModule):
    menu_title = "Sensors"
    sensors = {}
    current = 0

    def __init__(self, *args, **kwargs):
        super(TinkerforgeSensorModule, self).__init__(*args, **kwargs)
        self.update_sensors()

    def draw(self):
        if self.controller.screen and self.controller.current_module == self:
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
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "temp"))
        elif device_identifier == 217:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "ir_temp"))
        elif device_identifier == 27:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "humidity"))
        elif device_identifier == 259:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "light"))
        elif device_identifier == 238:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "sound"))
        elif device_identifier == 262:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "co2"))
        elif device_identifier == 227:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "voltage"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "current"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "power"))
        elif device_identifier == 25:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "dist"))
        elif device_identifier == 243:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "colour"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "colour_temp"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "colour_illuminance"))
        elif device_identifier == 221:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "air_pressure"))
        elif device_identifier == 241:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "reflectivity"))
        elif device_identifier == 240:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "magfield"))
        elif device_identifier == 250:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid,"acceleration_xyz"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "acceleration_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "acceleration_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "acceleration_Z"))
        elif device_identifier == 232:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "moisture"))
        elif device_identifier == 265:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "uv"))
        elif device_identifier == 26:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "dual_relay"))
        elif device_identifier == 233:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "motion"))
        elif device_identifier == 230:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "dual_button_state"))
        elif device_identifier == 282:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rgb_led_button_colour"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rgb_led_button_state"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rgb_led_button_colour_r"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rgb_led_button_colour_g"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rgb_led_button_colour_b"))
        elif device_identifier == 292:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "motion_2"))
        elif device_identifier == 215:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rotation_poti"))
        elif device_identifier == 239:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "tilt"))
        elif device_identifier == 229:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "dist_us"))
        elif device_identifier == 294:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "rotation_encoder_2"))
        elif device_identifier == 213:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "linear_poti"))
        elif device_identifier == 278:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "thermal_image"))
        elif device_identifier == 241:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "reflectivity"))
        elif device_identifier == 283:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "humidity_temp"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "humidity_v2"))
        elif device_identifier == 18:
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "heading"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "roll"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "pitch"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "linear_acceleration_Z"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "linear_acceleration_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "linear_acceleration_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "gravity_acceleration_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "gravity_acceleration_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "gravity_acceleration_Z"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "IMU_leds"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "IMU_acceleration_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "IMU_acceleration_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "IMU_acceleration_Z"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "angular_velocity_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "angular_velocity_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "angular_velocity_Z"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "linear_acceleration_xyz"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "gravity_acceleration_xyz"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "IMU_acceleration_xyz"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "angular_velocity_xyz"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "quaternion_W"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "quaternion_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "quaternion_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "quaternion_Z"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "IMU_temp"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "magnetic_field_X"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "magnetic_field_Y"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "magnetic_field_Z"))
            sensors.append(TinkerforgeSensor(
                self.ipcon, uid, "magnetic_field_xyz"))
        for sensor in sensors:
            self.sensors[sensor.sensor_type + "_" + uid] = sensor
	
    def callback_request_sensor_metadata(self):
        self.push({"type": "input", "data": self.sensors})

    def navigate(self, data):
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
        self.wait(1)
