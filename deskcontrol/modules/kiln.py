from navigation import StateModule
from datetime import datetime


class KilnModule(StateModule):
    menu_title = "Kiln"

    def __init__(self, controller):
        super(KilnModule, self).__init__(controller)
        self.controller.scheduler.enter(30, 1, self.update_kiln, (),)

    def build_sensor_list(self):
        self.sensor_list = {}
        if "SensorModule" in self.controller.modules:
            sensors = self.controller.modules["SensorModule"].sensors
            for pk in sensors:
                self.sensor_list[pk] = {}
                for attr in [
                        "uid", "sensor_type", "brick_tag", "units",
                        "update_time", "publish_limit", "variance", ]:
                    if hasattr(sensors[pk], attr):
                        self.sensor_list[pk][attr] = getattr(sensors[pk], attr)
        self.updated = datetime.now()
        return self.sensor_list

    def update_kiln(self):
        self.build_sensor_list()
        self.controller.event("kiln-publish", self.sensor_list)
        self.controller.scheduler.enter(600, 1, self.update_kiln, (),)
