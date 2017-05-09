from tinkerforge.bricklet_dual_relay import BrickletDualRelay
from navigation import StateModule
from config import RELAY_POSITIONS, DESK_ID

class PowerModule(StateModule):
    name = "power"
    controller = None
    relays = {}
    current = 0
    afk = False

    def __init__(self, controller):
        self.controller = controller
        super(PowerModule, self).__init__(controller)
        print "Created PowerModule"


    def draw(self, clear=True):
        if clear:
            self.controller.screen.device.clear_display()
        if not len(self.relays):
            self.controller.ipcon.enumerate()
            self.controller.screen.draw("values", {})
            return
        relays = self.relays[self.relays.keys()[self.current]]
        self.controller.screen.device.write_line(2, 0, "  " + relays["name"])
        state = relays["instance"].get_state()[relays["relay"]]
        if state: state = "Off"
        else: state = "On "
        self.controller.screen.device.write_line(
            4, 0, "  " + str(state))


    def switch_relay(self):
        if self.relays:
            relays = self.relays[self.relays.keys()[self.current]]
            state = relays["instance"].get_state()
            if relays["relay"]:
                relays["instance"].set_state(state[0], not state[1])
            else:
                relays["instance"].set_state(not state[0], state[1])
            self.draw(False)


    def power_off(self):
        if not self.afk:
            self.afk = True
            for relay in self.relays:
                #  TODO: Less hacky pls
                self.relays[relay]["instance"].set_state(False, True)


    def power_on(self):
        if self.afk:
            self.afk = False
            for relay in self.relays:
                #  TODO: Less hacky pls
                self.relays[relay]["instance"].set_state(False, False)


    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 26:
            self.relays["relay"+position] = {
                "instance": BrickletDualRelay(uid, self.controller.ipcon),
                "name": RELAY_POSITIONS[position][0],
                "relay": 0,
            }
            self.relays["relay"+position+"+"] = {
                "instance": self.relays["relay"+position]["instance"],
                "name": RELAY_POSITIONS[position][1],
                "relay": 1,
            }
            self.relays["relay"+position]["instance"] = DESK_ID
            print "Created Relay"


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
                self.current = len(self.relays)-1
            # print "Output: " + str(list(self.outputs)[self.current])
            self.draw()


    def tick(self):
        self.draw(clear=False)
