from navigation import StateModule


class IdentityModule(StateModule):
    name = "identity"
    controller = None

    def __init__(self, controller):
        self.controller = controller
        super(IdentityModule, self).__init__(controller)
        print("Created IdentityModule")

    def draw(self, clear=True):
        pass

    def try_bricklet(self, uid, device_identifier, position):
        pass

    def navigate(self, direction):
        pass

    def tick(self):
        pass
