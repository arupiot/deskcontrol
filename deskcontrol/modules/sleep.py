from navigation import StateModule
from datetime import datetime
from helpers import seconds_past
from modules.sensors import Sensor


class SleepModule(StateModule):
    always_tick = True
    last_motion = datetime.now()
    poweroff = 60
    awake = True

    def __init__(self, controller):
        super(SleepModule, self).__init__(controller)
        controller.event_handlers.append(self.event_handler)
        self.check_sleep()

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 233:
            sensor = Sensor(self.controller, "motion", uid)
            sensor.change_callbacks.append(self.motion_changed)
        if sensor and "SensorModule" in self.controller.modules:
            self.controller.modules["SensorModule"].sensors[sensor.uid] = (
                sensor)

    def motion_changed(self, value):
        if not hasattr(self, "previous"):
            self.previous = value
        if value:
            self.last_motion = datetime.now()
        if value and not self.previous:
            self.controller.event("wake", True)

    def check_sleep(self):
        if self.awake:
            if seconds_past(self.last_motion, self.poweroff):
                self.controller.event("sleep", True)
        self.controller.scheduler.enter(60, 1, self.check_sleep, (),)

    def event_handler(self, name, data):
        if name == "sleep":
            self.awake = False
        if name == "wake":
            self.awake = True
