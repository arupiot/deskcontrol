from navigation import StateModule


class BrickModule(StateModule):
    name = "brick"
    controller = None

    def __init__(self, controller):
        self.controller = controller
        super(BrickModule, self).__init__(controller)

    def add_sensor(self, sensor):
        pass
