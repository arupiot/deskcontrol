from navigation import StateModule
from sensors import Sensor

OUTLETS = {
    "rCr_Relay_Sensor0": "Laptop",
    "rCr_Relay_Sensor1": "Monitor",
}


class DCPowerModule(StateModule):
    menu_title = "Power"
    relays = {}
    current = 0

    def __init__(self, controller):
        super(DCPowerModule, self).__init__(controller)
        controller.add_event_handler("sleep", self.on_sleep)
        controller.add_event_handler("wake", self.on_wake)

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
            name = self.controller.localdb.get(key)
        if not name and key in OUTLETS:
            name = OUTLETS[key]
        if not name:
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

    def on_sleep(self, data):
        for relay in self.relays:
            #  TODO: Less hacky pls
            pass
            # self.relays[relay].instance.set_state(False, True)

    def on_wake(self, data):
        for relay in self.relays:
            #  TODO: Less hacky pls
            pass
            # self.relays[relay].instance.set_state(False, False)

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 26:
            s = Sensor(self.controller, "dualrelay", uid)
            for instance in ["0", "1"]:
                self.relays[s.uid + instance] = s

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
