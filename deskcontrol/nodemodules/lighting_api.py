from iotnode.module import NodeModule
import requests
import logging


class LightingAPIModule(NodeModule):
    outputs = {}
    edit = False
    current = 0
    intens = 100
    color = 0
    colors = [
        {"name": "Default", "color": "FFFF33"},
        {"name": "Red", "color": "FF0000"},
        {"name": "Blue", "color": "0000FF"},
        {"name": "Magenta", "color": "FF00FF"},
        {"name": "Green", "color": "00FF00"},
        {"name": "Orange", "color": "FFCC00"},
    ]

    def __init__(self, *args, **kwargs):
        super(LightingAPIModule, self).__init__(*args, **kwargs)
        self.set_light()
        self.outputs["taskcol"] = {
            "name": "'R' LED Colour",
            "type": "select",
        }
        self.add_to_menu("Lighting")

    def draw(self):
        outputs = self.outputs[self.outputs.keys()[self.current]]
        if self.edit:
            name = outputs["name"] + "*"
        else:
            name = outputs["name"]
        if outputs["type"] == "dimmer":
            self.push({"type": "render_data", "data": {
                "values",
                {"title": name,
                 "value": str(self.intens) + " %", }}})
        if outputs["type"] == "select":
            self.push({"type": "render_data", "data": {
                "values",
                {"title": name,
                 "value": str(self.colors[self.color]["name"]), }}})

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
        self.set_light()

    def set_light(self):
        color = self.colors[self.color]["color"]
        intens = int(float(self.intens) / 100 * 255)
        try:
            requests.get(
                'http://192.168.2.101:8000/color/4/%s/' % color,
                timeout=0.5)
            requests.get(
                'http://192.168.2.101:8000/level/4/%s/' % intens,
                timeout=0.5)
        except Exception as e:
            logging.error("Error pushing lighting values" + str(e))

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
                self.draw()
        else:
            if direction in ["back", "left"]:
                self.edit = False
                self.draw()
            if direction in ["down", "up"]:
                self.change_light(direction)
                self.draw()
