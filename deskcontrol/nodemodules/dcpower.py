from iotnode.module import NodeModule
from sensors import Sensor

OUTLETS = {
    "rCr_Relay_Sensor0": "Laptop",
    "rCr_Relay_Sensor1": "Monitor",
}


class DCPowerModule(NodeModule):
    relays = {}
    current = 0

    def __init__(self, *args, **kwargs):
        super(DCPowerModule, self).__init__(*args, **kwargs)
        self.add_to_menu("Power")

    def draw(self):
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
        if key in OUTLETS:
            name = OUTLETS[key]
        if not name:
            name = relay.name
        self.push({"type": "render_data", "data": {
            "title": name, "value": str(state), }})

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

    def callback_sleep(self, data):
        if 'sleep' in data:
            for relay in self.relays:
                self.relays[relay].instance.set_state(False, True)
        if 'wake' in data:
            for relay in self.relays:
                self.relays[relay].instance.set_state(False, False)

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 26:
            s = Sensor(self.controller, "dualrelay", uid)
            for instance in ["0", "1"]:
                self.relays[s.uid + instance] = s

    def navigate(self, data):
        direction = data["data"]
        if direction in ["back", "left"]:
            self.push({"type": "input", "switch": "MenuModule"})
        if direction in ["enter", "right"]:
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
            self.draw()
