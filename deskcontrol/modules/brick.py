from navigation import StateModule
from datetime import datetime


class BrickModule(StateModule):
    menu_title = "Brick"

    def __init__(self, controller):
        super(BrickModule, self).__init__(controller)
        self.update_brick()

    def build_sensor_list(self):
        self.sensor_list = []
        # if "SensorModule" in self.controller.modules:
        #     sensors = self.controller.modules["SensorModule"].sensors
        #     for pk in sensors:
        #         self.sensor_list.append(sensors[pk])
        self.updated = datetime.now()
        return self.sensor_list

    def update_brick(self):
        self.build_sensor_list()
        self.controller.publish("brick", self.sensor_list)
        self.controller.scheduler.enter(600, 1, self.update_brick, (),)
