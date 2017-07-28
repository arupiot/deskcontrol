from navigation import StateModule
from datetime import datetime, timedelta
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector


class SchedulerModule(StateModule):
    controller = None
    detector = None
    always_tick = True

    last_motion = None
    poweroff = 1

    def __init__(self, controller):
        self.controller = controller
        super(SchedulerModule, self).__init__(controller)

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 233:
            self.setup_detection(uid)
            print("Setup Motion Detection for PIR")
        else:
            self.setup_detection(uid)
            print("Setup Motion Detection for other motion device")

    def push_value(self):
        if "InfluxModule" in self.controller.modules:
            self.controller.modules["InfluxModule"].push_value(
                str(self.detector["brick"]),
                self.detector["value"],
                {"type": self.detector["type"], })

    def push_raw(self, value):
        if "InfluxModule" in self.controller.modules:
            self.controller.modules["InfluxModule"].push_value(
                str(self.detector["brick"] + "_raw"),
                value,
                {"type": self.detector["type"], })

    def motion_detected(self):
        self.last_motion = datetime.now()
        # print(self.detector)
        prev = None
        if self.detector:
            prev = self.detector["value"]
        self.detector["value"] = "True"
        if "PowerModule" in self.controller.modules:
            self.controller.modules["PowerModule"].power_on()
            self.controller.modules["LightingModule"].set_light()
        if not prev:
            self.push_value()
        self.push_raw("True")

    def motion_ended(self):
        self.push_raw("False")

    def setup_detection(self, uid):
        # self.detector.register_callback(
        #    self.detector.CALLBACK_DETECTION_CYCLE_ENDED,
        #    self.detection_cycle_ended)
        self.detector = {
            "instance": BrickletMotionDetector(uid, self.controller.ipcon),
            "name": "Detector",
            "type": "pir",
            "brick": "Motion_Sensor",
            "value": None,
        }
        self.detector["instance"].register_callback(
            self.detector["instance"].CALLBACK_MOTION_DETECTED,
            self.motion_detected)

        self.detector["instance"].register_callback(
            self.detector["instance"].CALLBACK_DETECTION_CYCLE_ENDED,
            self.motion_ended)

        if "BrickModule" in self.controller.modules:
            self.controller.modules["BrickModule"].add_sensor(self.detector)

    def tick(self):
        if self.last_motion and "instance" in self.detector:
            if (self.last_motion < datetime.now() -
                    timedelta(minutes=self.poweroff)):
                print("No motion detected - turning off")
                self.last_motion = None
                self.detector["value"] = "False"
                self.push_value()
                if "PowerModule" in self.controller.modules:
                    self.controller.modules["PowerModule"].power_off()
