from iotnode.module import NodeModule
from datetime import datetime, timedelta


class KilnModule(NodeModule):
    sensor_list = {}
    changed = False
    last_request = datetime.now() + timedelta(seconds=20)

    def callback_sensor_metadata(self, data):
        self.changed = True
        self.sensor_list = {}
        sensors = data["data"]
        for pk in sensors:
            self.sensor_list[pk] = {}
            for attr in [
                    "uid", "sensor_type", "brick_tag", "units",
                    "update_time", "publish_limit", "variance", ]:
                if hasattr(sensors[pk], attr):
                    self.sensor_list[pk][attr] = getattr(sensors[pk], attr)
        self.updated = datetime.now()
        return self.sensor_list


    def tick(self):
        if self.last_request <= datetime.now():
            self.push({"type": "request_sensor_metadata", })
            self.last_request = datetime.now() + timedelta(minutes=10)
        if self.sensor_list and self.changed:
            self.push({"type": "kiln_publish", "data": self.sensor_list})
            self.changed = False
        self.wait(1)
