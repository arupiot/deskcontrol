from navigation import StateModule
from sensors import Sensor


class PowerModule(StateModule):
    menu_title = "Power"
    relays = {}
    current = 0

    def __init__(self, controller):
        super(PowerModule, self).__init__(controller)
        controller.event_handlers.append(self.event_handler)

    def draw(self, clear=True):
        if clear:
            self.controller.screen.device.clear_display()
        if not len(self.relays):
            self.controller.ipcon.enumerate()
            self.controller.screen.draw("values", {})
            return
        key = self.relays.keys()[self.current]
        relay = self.relays[key]
        state = relay.instance.get_state()[int(key[-1:])]
        if state:
            state = "Off"
        else:
            state = "On "
        if self.controller.localdb:
            unique_name = self.controller.localdb.get(relay.uid)
        if unique_name:
            name = unique_name
        else:
            name = relay.name
        self.controller.screen.draw(
            "values",
            {"title": name, "value": str(state), })

    def switch_relay(self):
        if self.relays:
            key = self.relays.keys()[self.current]
            relay = self.relays[key]
            state = relay.instance.get_state()
            if int(key[-1:]):
                relay.instance.set_state(state[0], not state[1])
            else:
                relay.instance.set_state(not state[0], state[1])
            self.draw(False)

    def event_handler(self, name, data):
        if name == "sleep":
            for relay in self.relays:
                #  TODO: Less hacky pls
                self.relays[relay].instance.set_state(False, True)
        if name == "wake":
            for relay in self.relays:
                #  TODO: Less hacky pls
                self.relays[relay].instance.set_state(False, False)

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 26:
            s = Sensor(self.controller, "dualrelay", uid)
            # Todo: labelling
            self.relays[s.uid + "_0"] = s
            self.relays[s.uid + "_1"] = s

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
