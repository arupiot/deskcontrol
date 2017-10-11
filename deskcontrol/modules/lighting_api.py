from navigation import StateModule


class LightingAPIModule(StateModule):
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

    def __init__(self, controller):
        super(LightingAPIModule, self).__init__(controller)
        self.set_light()

    def draw(self, clear=True):
        if clear:
            self.controller.screen.device.clear_display()
        if not len(self.outputs):
            self.controller.ipcon.enumerate()
            self.controller.screen.draw("values", {})
            return
        outputs = self.outputs[self.outputs.keys()[self.current]]

        if outputs["type"] == "dimmer":
            self.controller.screen.draw(
                "values",
                {"title": outputs["name"],
                 "value": str(self.intens) + " %", })
        if outputs["type"] == "select":
            self.controller.screen.draw(
                "values",
                {"title": outputs["name"],
                 "value": str(self.colors[self.color]["name"]), })

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
        # print "change " + direction + str(self.color)

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

        self.controller.scheduler.enter(1, 1, self.set_light, (),)

    def navigate(self, direction):
        output = self.outputs[self.outputs.keys()[self.current]]
        if not self.edit:
            if direction == "forward":
                self.edit = True
                output["name"] = output["name"] + " *"
                self.draw()
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
                    self.current = len(self.outputs) - 1
                # print "Output: " + str(list(self.outputs)[self.current])
                self.draw()
        else:
            if direction == "back":
                self.edit = False
                output["name"] = output["name"][:-1]
                self.draw()
            if direction in ["down", "up"]:
                self.change_light(direction)
                self.draw()

    def tick(self):
        self.draw(clear=False)
