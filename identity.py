from navigation import StateModule
from config import SHORT_IDENT, INFLUX_AUTH


class IdentityModule(StateModule):
    name = "identity"
    controller = None

    def __init__(self, controller):
        self.controller = controller
        super(IdentityModule, self).__init__(controller)
        # print(get_config())

        # Influx Auth should come from identify system, not config
        # Currently relys on order of modules being loaded to be correct...
        if "InfluxModule" in self.controller.modules:
            self.controller.modules["InfluxModule"].connect(INFLUX_AUTH)

    def get_ident(self):
        return SHORT_IDENT
