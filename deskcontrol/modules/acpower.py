from navigation import StateModule
import energenie

OUTLETS = {
    1: {
        "name": "Laptop",
        "instance": energenie.Devices.ENER002(1),
    },
    2: {
        "name": "Monitor 1",
        "instance": energenie.Devices.ENER002(2),
    },
    3: {
        "name": "Monitor 2",
        "instance": energenie.Devices.ENER002(3),
    },
}


class Outlet():
    def __init__(self, outlet, controller):
        energenie.init()
        self.state = True
        if controller.localdb:
            unique_name = controller.localdb.get("outlet-" + str(outlet))
        if unique_name:
            self.name = unique_name
        else:
            self.name = OUTLETS[outlet]["name"]
        self.instance = OUTLETS[outlet]["instance"]

    def on(self):
        if not self.state:
            self.instance.turn_on()
            self.state = True

    def off(self):
        if self.state:
            self.instance.turn_off()
            self.state = False

    def switch(self):
        if self.state:
            self.off()
        else:
            self.on()


class ACPowerModule(StateModule):
    menu_title = "Power"
    outlets = {}
    current = 1

    def __init__(self, controller):
        super(ACPowerModule, self).__init__(controller)
        controller.add_event_handler("sleep", self.on_sleep)
        controller.add_event_handler("wake", self.on_wake)
        for outlet in OUTLETS:
            self.outlets[outlet] = Outlet(outlet, controller)

    def draw(self, clear=True):
        if clear:
            self.controller.screen.device.clear_display()
        if not len(self.outlets):
            self.controller.ipcon.enumerate()
            self.controller.screen.draw("values", {})
            return
        key = self.outlets.keys()[self.current]
        outlet = self.outlets[key]
        if outlet.state:
            state = "On "
        else:
            state = "Off"
        self.controller.screen.draw(
            "values",
            {"title": outlet.name, "value": str(state), })

    def switch_relay(self):
        if self.outlets:
            key = self.outlets.keys()[self.current]
            self.outlets[key].switch()
            self.draw(False)

    def on_sleep(self, data):
        for outlet in self.outlets:
            # TODO: Less hacky!
            if outlet != 1:
                self.outlets[outlet].off()

    def on_wake(self, data):
        for outlet in self.outlets:
            self.outlets[outlet].on()

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
            if self.current >= len(self.outlets):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.outlets) - 1
            # print("Output: " + str(list(self.outputs)[self.current]))
            self.draw()

    def tick(self):
        self.draw(clear=False)
