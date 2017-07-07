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
            # print("Setup Motion Detection")

    def motion_detected(self):
        self.last_motion = datetime.now()
        if "PowerModule" in self.controller.modules:
            self.controller.modules["PowerModule"].power_on()
            self.controller.modules["LightingModule"].set_light()
        # print("Motion Detected")

    # def detection_cycle_ended(self):
    #    print("Detection Cycle Ended")

    def setup_detection(self, uid):
        # self.detector.register_callback(
        #    self.detector.CALLBACK_DETECTION_CYCLE_ENDED,
        #    self.detection_cycle_ended)
        self.detector = {
            "instance": BrickletMotionDetector(uid, self.controller.ipcon),
            "name": "Detector",
            "type": "pir",
        }
        self.detector["instance"].register_callback(
            self.detector["instance"].CALLBACK_MOTION_DETECTED,
            self.motion_detected)
        if "InfluxModule" in self.controller.modules:
            self.controller.modules["InfluxModule"].add_sensor(self.detector)
        if "BrickModule" in self.controller.modules:
            self.controller.modules["BrickModule"].add_sensor(self.detector)

    def tick(self):
        if self.last_motion and "instance" in self.detector:
            if (self.last_motion < datetime.now() -
                    timedelta(minutes=self.poweroff)):
                print("No motion detected - turning off")
                self.last_motion = None
                if "PowerModule" in self.controller.modules:
                    self.controller.modules["PowerModule"].power_off()
