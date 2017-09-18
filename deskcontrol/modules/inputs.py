from tinkerforge.bricklet_joystick import BrickletJoystick
from tinkerforge.bricklet_multi_touch import BrickletMultiTouch
from navigation import StateModule


class InputModule(StateModule):
    inputs = {}

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 210:
            self.inputs["joystick"] = BrickletJoystick(
                uid, self.controller.ipcon)
            self.inputs["joystick"].set_debounce_period(400)
            self.inputs["joystick"].register_callback(
                self.inputs["joystick"].CALLBACK_POSITION_REACHED,
                self.joystick_position)
            self.inputs["joystick"].register_callback(
                self.inputs["joystick"].CALLBACK_PRESSED,
                self.joystick_pushed)
            self.inputs["joystick"].set_position_callback_threshold(
                "o", -99, 99, -99, 99)
            print("Created Joystick Input")
        if device_identifier == 234:
            self.inputs["multitouch"] = BrickletMultiTouch(
                uid, self.controller.ipcon)
            self.inputs["multitouch"].set_electrode_sensitivity(125)
            self.inputs["multitouch"].register_callback(
                self.inputs["multitouch"].CALLBACK_TOUCH_STATE,
                self.multitouch)
            print("Created Multitouch Input")

    def joystick_position(self, x, y):
        print("Joystick Position: ", x, y)
        if "SchedulerModule" in self.controller.modules:
            self.controller.modules["SchedulerModule"].motion_detected()
        if y == 100:
            self.controller.navigate("up")
        elif y == -100:
            self.controller.navigate("down")

        if x == 100:
            self.controller.navigate("back")
        elif x == -100:
            self.controller.navigate("forward")

    def joystick_pushed(self):
        print("Joystick Pushed")
        self.controller.navigate("forward")

    def multitouch(self, state):
        if "SchedulerModule" in self.controller.modules:
            self.controller.modules["SchedulerModule"].motion_detected()
        if state & (1 << 12):
            pass
        if (state & 0xfff) == 0:
            pass
        else:
            try:
                if state & (1 << 0):
                    self.controller.navigate("forward")
                if state & (1 << 1):
                    self.controller.navigate("back")
                if state & (1 << 2):
                    self.controller.navigate("up")
                if state & (1 << 3):
                    self.controller.navigate("down")
            except Exception:
                pass
