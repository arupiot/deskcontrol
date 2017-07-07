from navigation import StateModule


class CommanderModule(StateModule):
    name = "commander"
    controller = None

    def __init__(self, controller):
        self.controller = controller
        super(CommanderModule, self).__init__(controller)
