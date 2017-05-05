from navigation import StateModule
from datetime import datetime, timedelta
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector

class SchedulerModule(StateModule):
    controller = None
    detector = None
    always_tick = True

    last_motion = None
    poweroff = 2

    def __init__(self, controller):
        self.controller = controller
        super(SchedulerModule, self).__init__(controller)
        print "Created SchedulerModule"


    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 233:
            self.setup_detection(uid)
            print "Setup Motion Detection"


    def motion_detected(self):
        self.last_motion = datetime.now()
        if "PowerModule" in self.controller.modules:
            self.controller.modules["PowerModule"].power_on()
        #print("Motion Detected")


    #def detection_cycle_ended(self):
    #    print("Detection Cycle Ended")


    def setup_detection(self, uid):
        self.detector = BrickletMotionDetector(uid, self.controller.ipcon)
        self.detector.register_callback(
            self.detector.CALLBACK_MOTION_DETECTED, self.motion_detected)
        #self.detector.register_callback(
        #    self.detector.CALLBACK_DETECTION_CYCLE_ENDED,
        #    self.detection_cycle_ended)


    def tick(self):
        if self.last_motion:
            if (self.last_motion < datetime.now() -
                    timedelta(minutes = self.poweroff)):
                print "No motion detected - turning off"
                self.last_motion = None
                if "PowerModule" in self.controller.modules:
                    self.controller.modules["PowerModule"].power_off()
