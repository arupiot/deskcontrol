from navigation import StateModule
from datetime import datetime, timedelta
from sensors import Sensor


class MotionSensor(Sensor):
    def callback(self, value):
        self.value = value
        self.updated = datetime.now()
        self.publish()


class SchedulerModule(StateModule):
    detector = None
    always_tick = True

    last_motion = None
    poweroff = 1

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 233:
            self.detector = MotionSensor(self.controller, "motion", uid)

    def publish_raw(self, value):
        if self.detector:
            self.controller.publish(
                self.detector.uid + "_raw", str(value))

    def motion_detected(self):
        self.last_motion = datetime.now()
        # print(self.detector)
        prev = None
        if self.detector:
            prev = self.detector.value
            self.detector.value = 1
        if "PowerModule" in self.controller.modules:
            self.controller.modules["PowerModule"].power_on()
        if "LightingModule" in self.controller.modules:
            self.controller.modules["LightingModule"].set_light()
        if not prev and self.detector:
            self.detector.publish()
        self.publish_raw(1)

    def motion_ended(self):
        self.publish_raw(0)

    def setup_detection(self, uid):
        i = self.detector.instance
        i.register_callback(i.CALLBACK_MOTION_DETECTED,
                            self.motion_detected)
        i.register_callback(i.CALLBACK_DETECTION_CYCLE_ENDED,
                            self.motion_ended)

        if "BrickModule" in self.controller.modules:
            self.controller.modules["BrickModule"].add_sensor(self.detector)

    def tick(self):
        if self.detector and self.last_motion and hasattr(
                self.detector, "instance"):
            if (self.last_motion < datetime.now() -
                    timedelta(minutes=self.poweroff)):
                print("No motion detected - turning off")
                self.last_motion = None
                self.detector.value = 0
                self.detector.publish()
                if "PowerModule" in self.controller.modules:
                    self.controller.modules["PowerModule"].power_off()
