from navigation import StateModule
from sensors import Sensor


class PowerModule(StateModule):
    menu_title = "Power"
    relays = {}
    current = 0
    afk = False

    def draw(self, clear=True):
        if clear:
            self.controller.screen.device.clear_display()
        if not len(self.relays):
            self.controller.ipcon.enumerate()
            self.controller.screen.draw("values", {})
            return
        relays = self.relays[self.relays.keys()[self.current]]
        state = relays["instance"].get_state()[relays["relay"]]
        if state:
            state = "Off"
        else:
            state = "On "

        self.controller.screen.draw(
            "values",
            {"title": relays["name"], "value": str(state), })

    def switch_relay(self):
        if self.relays:
            relay = self.relays[self.relays.keys()[self.current]]
            state = relay.instance.get_state()
            if relay.instance:
                relay.instance.set_state(state[0], not state[1])
            else:
                relay.instance.set_state(not state[0], state[1])
            self.draw(False)
            if "LightingModule" in self.controller.modules:
                self.controller.modules["LightingModule"].set_light()

    def power_off(self):
        if not self.afk:
            self.afk = True
            for relay in self.relays:
                #  TODO: Less hacky pls
                self.relays[relay].instance.set_state(False, True)

    def power_on(self):
        if self.afk:
            self.afk = False
            for relay in self.relays:
                #  TODO: Less hacky pls
                self.relays[relay].instance.set_state(False, False)

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 26:
            for x in ["relay_a", "relay_b"]:
                s = Sensor(self.controller, x, uid)
                self.relays[s.uid] = s

    def navigate(self, direction):
        if direction == "back":
            self.controller.prev_module()
        if direction == "forward":
            self.switch_relay()
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.relays):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.relays) - 1
            # print("Output: " + str(list(self.outputs)[self.current]))
            self.draw()

    def tick(self):
        self.draw(clear=False)
