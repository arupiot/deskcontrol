from classes.tfmodule import TinkerForgeModule
from datetime import datetime
from helpers import seconds_past
from classes.tfsensor import TinkerforgeSensor


class SleepModule(TinkerForgeModule):
    last_motion = datetime.now()
    sleeptime = 150
    awake = True
    sensor = None

    def __init__(self, *args, **kwargs):
        super(SleepModule, self).__init__(*args, **kwargs)
        if "sleep_time" in self.cache:
            self.sleeptime = self.cache["sleep_time"]

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 233:
            self.sensor = TinkerforgeSensor(uid, "motion", self.connection)
            self.sensor.change_callbacks.append(self.motion_changed)
        if self.sensor and "SensorModule" in self.controller.modules:
            self.controller.modules["SensorModule"].sensors[
                self.sensor.uid] = (self.sensor)

    def motion_changed(self, value):
        if not hasattr(self, "previous"):
            self.previous = value
        if value and not self.awake:
            self.push({"type": "sleep", "wake": True})
        if value:
            self.last_motion = datetime.now()

    def callback_input(self, data):
        if not self.awake:
            self.push({"type": "sleep", "wake": True})
            self.last_motion = datetime.now()

    def callback_sleep(self, data):
        if 'sleep' in data:
            self.awake = False
        if 'wake' in data:
            self.awake = True

    def tick(self):
        if self.awake and self.sensor:
            if seconds_past(self.last_motion, self.sleeptime):
                self.push({"type": "sleep", "sleep": True})
        self.wait(1)
