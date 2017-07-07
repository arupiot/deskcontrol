from navigation import StateModule


class BrickModule(StateModule):
    name = "brick"
    controller = None

    def __init__(self, controller):
        self.controller = controller
        super(BrickModule, self).__init__(controller)
        print("Created BrickModule")

    def draw(self, clear=True):
        pass

    def try_bricklet(self, uid, device_identifier, position):
        pass

    def navigate(self, direction):
        pass

    def tick(self):
        pass

    def add_sensor(self, sensor):
        pass
