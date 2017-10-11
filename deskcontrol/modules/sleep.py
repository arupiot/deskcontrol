from navigation import StateModule
from datetime import datetime
from helpers import seconds_past
from modules.sensors import Sensor


class SleepModule(StateModule):
    last_motion = datetime.now()
    poweroff = 150
    awake = True
    sensor = None

    def __init__(self, controller):
        super(SleepModule, self).__init__(controller)
        controller.add_event_handler("sleep", self.on_sleep)
        controller.add_event_handler("wake", self.on_wake)
        self.check_sleep()

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 233:
            self.sensor = Sensor(self.controller, "motion", uid)
            self.sensor.change_callbacks.append(self.motion_changed)
        if self.sensor and "SensorModule" in self.controller.modules:
            self.controller.modules["SensorModule"].sensors[
                self.sensor.uid] = (self.sensor)

    def motion_changed(self, value):
        if not hasattr(self, "previous"):
            self.previous = value
        if value and not self.awake:
            self.controller.event("wake", True)
        if value:
            self.last_motion = datetime.now()

    def check_sleep(self):
        if self.awake and self.sensor:
            if seconds_past(self.last_motion, self.poweroff):
                self.controller.event("sleep", True)
        self.controller.scheduler.enter(60, 1, self.check_sleep, (),)

    def on_sleep(self, data):
        self.awake = False

    def on_wake(self, data):
        self.awake = True
