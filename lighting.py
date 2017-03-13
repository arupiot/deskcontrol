from navigation import StateModule
from config import LIGHTING_IP
import requests

actions = [
    ("task", "Task Lighting"),
    ("warm", "Warm Uplight"),
    ("cool", "Cool Uplight"),
]


class LightingModule(StateModule):
    name = "Lighting Control"
    controller = None
    current = 0
    editing = False
    values = {}

    def __init__(self, controller):
        self.controller = controller
        super(LightingModule, self).__init__(controller)
        print "Created LightingModule"

    def draw(self, clear=True):
        if not self.controller.screen:
            return
        try:
            if clear:
                self.controller.screen.clear_display()
                if not requests.get('http://' + LIGHTING_IP + '/arduino/'):
                    self.controller.screen.write_line(
                        3, 0,
                        "  can't connect to controller")
                return
            action = actions[self.current][0]
            value = requests.get('http://' + LIGHTING_IP + '/arduino/' +
                                 action + '/')
            self.values[action] = value
            self.controller.screen.write_line(
                2, 0, "  " + actions[self.current][1])
            self.controller.screen.write_line(
                4, 0, "  " + str(round(value / 255 * 100)) + " %")
        except:
            self.controller.screen.clear_display()
            self.controller.screen.write_line(
                3, 0,
                "  can't connect to controller")

    def change_value(self, direction):
        pass

    def navigate(self, direction):
        if direction == "back":
            if self.editing:
                self.editing = False
            else:
                self.controller.prev_module()
        if direction in ["down", "up"]:
            if self.editing:
                action = actions[self.current][0]
                value = self.values[action]
                if direction == "down":
                    value = value - 13
                else:
                    value = value + 13
                requests.get('http://' + LIGHTING_IP + '/arduino/' +
                             action + '/' + str(round(value)))
            else:
                if direction == "down":
                    self.current = self.current + 1
                else:
                    self.current = self.current - 1
                if self.current >= len(actions):
                    self.current = 0
                elif self.current < 0:
                    self.current = len(actions) - 1
            self.draw()
        else:
            self.editing = True

    def tick(self):
        self.draw(clear=False)
