from tinkerforge.bricklet_led_strip import BrickletLEDStrip
from iotnode.module import NodeModule


class LightingModule(NodeModule):
    menu_title = "Lighting"

    outputs = {}
    edit = False
    device = None
    current = 0
    intens = 100
    color = 0
    colors = [
        {"name": "Warm", "color": (255, 160, 25)},
        {"name": "Cool", "color": (255, 255, 50)},
        {"name": "Red", "color": (255, 0, 0)},
        {"name": "Blue", "color": (0, 0, 255)},
        {"name": "Magenta", "color": (255, 0, 255)},
        {"name": "Green", "color": (0, 255, 0)},
    ]

    def __init__(self, *args, **kwargs):
        super(LightingModule, self).__init__(*args, **kwargs)
        self.set_light()
        self.add_to_menu("Lighting")

    def draw(self):
        if not len(self.outputs):
            self.push({"type": "render_data", "data": {}})
            return
        outputs = self.outputs[self.outputs.keys()[self.current]]
        if self.edit:
            name = outputs["name"] + "*"
        else:
            name = outputs["name"]
        if outputs["type"] == "dimmer":
            self.push({"type": "render_data", "data": {
                "title": name,
                "value": str(self.intens) + " %", }})
        if outputs["type"] == "select":
            self.push({"type": "render_data", "data": {
                "title": name,
                "value": str(self.colors[self.color]["name"]), }})

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 231 and "taskint" not in self.outputs:
            self.device = BrickletLEDStrip(uid, self.ipcon)
            self.outputs["taskint"] = {
                "name": "Task Intensity",
                "type": "dimmer",
            }
            self.outputs["taskcol"] = {
                "name": "Task Colour",
                "type": "select",
            }
            self.device.set_chip_type(self.device.CHIP_TYPE_WS2811)
            self.device.set_channel_mapping(self.device.CHANNEL_MAPPING_BRG)

    def change_light(self, direction):
        if self.outputs[self.outputs.keys()[self.current]]["type"] == "dimmer":
            if direction == "up" and self.intens < 100:
                self.intens += 10
            elif direction == "down" and self.intens > 0:
                self.intens -= 10
        else:
            if direction == "up":
                if self.color >= len(self.colors) - 1:
                    self.color = 0
                else:
                    self.color += 1
            elif direction == "down":
                if self.color <= 0:
                    self.color = len(self.colors) - 1
                else:
                    self.color -= 1

    def set_light(self):
        if self.device:
            color = self.colors[self.color]["color"]
            color = (int(color[0] * self.intens / 100),
                     int(color[1] * self.intens / 100),
                     int(color[2] * self.intens / 100))
            r = [color[0] for i in range(16)]
            b = [color[1] for i in range(16)]
            g = [color[2] for i in range(16)]
            self.device.set_rgb_values(0, 16, r, b, g)

            r = [255 for i in range(16)]
            b = [0 for i in range(16)]
            g = [0 for i in range(16)]
            self.device.set_rgb_values(17, 1, r, b, g)

    def callback_input(self, data):
        direction = data["data"]
        if not self.edit:
            if direction in ["enter", "right"]:
                self.edit = True
                self.draw()
            if direction in ["back", "left"]:
                self.push({"type": "input", "switch": "MenuModule"})
            if direction in ["down", "up"]:
                if direction == "down":
                    self.current = self.current + 1
                else:
                    self.current = self.current - 1
                if self.current >= len(self.outputs):
                    self.current = 0
                elif self.current < 0:
                    self.current = len(self.outputs) - 1
                # print "Output: " + str(list(self.outputs)[self.current])
                self.draw()
        else:
            if direction in ["back", "left"]:
                self.edit = False
                self.draw()
            if direction in ["down", "up"]:
                self.change_light(direction)
                self.draw()
