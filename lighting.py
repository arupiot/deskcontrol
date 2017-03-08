from tinkerforge.bricklet_analog_out_v2 import BrickletAnalogOutV2
from navigation import StateModule

class LightingModule(StateModule):
    name = "Lighting Control"
    controller = None
    outputs = {}
    current = 0

    def __init__(self, controller):
        self.controller = controller
        super(LightingModule, self).__init__(controller)
        print "Created LightingModule"


    def draw(self, clear=True):
        if clear:
            self.controller.screen.clear_display()
        if not len(self.outputs):
            self.controller.ipcon.enumerate()
            self.controller.screen.write_line(3, 0,
                "  no lighting controller")
            return
        outputs = self.outputs[self.outputs.keys()[self.current]]
        self.controller.screen.write_line(2, 0, "  " + outputs["name"])
        if outputs["type"] == "dimmer":
            percentage = outputs["instance"].get_output_voltage()/12000*100
            self.controller.screen.write_line(
                4, 0, "  " + str(percentage) + " %")


    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 256:
            self.outputs["task"] = {
                "instance": BrickletAnalogOutV2(uid, self.controller.ipcon),
                "name": "Task Lighting",
                "type": "dimmer",
            }
            print "Created Analogue Output"


    def navigate(self, direction):
        if direction == "back":
            self.controller.prev_module()
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.outputs):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.outputs)-1
            # print "Output: " + str(list(self.outputs)[self.current])
            self.draw()


    def tick(self):
        self.draw(clear=False)
