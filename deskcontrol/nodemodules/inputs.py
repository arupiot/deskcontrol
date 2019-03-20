from tinkerforge.bricklet_joystick import BrickletJoystick
from tinkerforge.bricklet_multi_touch import BrickletMultiTouch
from classes.tfmodule import TinkerForgeModule


class InputModule(TinkerForgeModule):
    inputs = {}

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 210:
            self.inputs["joystick"] = BrickletJoystick(
                uid, self.ipcon)
            self.inputs["joystick"].set_debounce_period(400)
            self.inputs["joystick"].register_callback(
                self.inputs["joystick"].CALLBACK_POSITION_REACHED,
                self.joystick_position)
            self.inputs["joystick"].register_callback(
                self.inputs["joystick"].CALLBACK_PRESSED,
                self.joystick_pushed)
            self.inputs["joystick"].set_position_callback_threshold(
                "o", -99, 99, -99, 99)
        if device_identifier == 234:
            self.inputs["multitouch"] = BrickletMultiTouch(
                uid, self.ipcon)
            self.inputs["multitouch"].set_electrode_sensitivity(125)
            self.inputs["multitouch"].register_callback(
                self.inputs["multitouch"].CALLBACK_TOUCH_STATE,
                self.multitouch)

    def navigate(self, direction):
        self.push({"type": "input", "data": direction})

    def joystick_position(self, x, y):
        if y == 100:
            self.navigate("up")
        elif y == -100:
            self.navigate("down")

        if x == 100:
            self.navigate("left")
        elif x == -100:
            self.navigate("right")

    def joystick_pushed(self):
        self.navigate("enter")

    def multitouch(self, state):
        if state & (1 << 12):
            pass
        if (state & 0xfff) == 0:
            pass
        else:
            try:
                if state & (1 << 0):
                    self.navigate("right")
                if state & (1 << 1):
                    self.navigate("left")
                if state & (1 << 2):
                    self.navigate("up")
                if state & (1 << 3):
                    self.navigate("down")
            except Exception:
                pass
