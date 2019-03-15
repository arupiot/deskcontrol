from iotnode.module import NodeModule
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


class ACPowerModule(NodeModule):
    outlets = {}
    current = 1

    def __init__(self, *args, **kwargs):
        super(ACPowerModule, self).__init__(*args, **kwargs)
        for outlet in OUTLETS:
            self.outlets[outlet] = Outlet(outlet)
        self.add_to_menu("Power")

    def draw(self):
        key = self.outlets.keys()[self.current]
        outlet = self.outlets[key]
        if outlet.state:
            state = "On"
        else:
            state = "Off"

        self.push({"type": "render_data", "data": {
            "title": outlet.name, "value": str(state), }})

    def switch_relay(self):
        if self.outlets:
            key = self.outlets.keys()[self.current]
            self.outlets[key].switch()
            self.draw(False)

    def callback_sleep(self, data):
        if 'sleep' in data:
            for outlet in self.outlets:
                # TODO: Less hacky!
                if outlet != 1:
                    self.outlets[outlet].off()
        if 'wake' in data:
            for outlet in self.outlets:
                self.outlets[outlet].on()

    def callback_input(self, data):
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
            if self.current >= len(self.outlets):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.outlets) - 1
            self.draw()
