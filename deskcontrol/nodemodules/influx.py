from iotnode.module import NodeModule
from influxdb import InfluxDBClient
from helpers import sensor_data_format
import logging

class InfluxModule(NodeModule):
    client = None
    
    def __init__(self, *args, **kwargs):
        super(InfluxModule, self).__init__(*args, **kwargs)

        if not "_INFLUX_AUTH" in self.cache:
            exit()
        self.connect(self.cache['_INFLUX_AUTH'])

    def connect(self, auth):
        try:
            self.client = InfluxDBClient(
                host=auth["host"],
                port=auth["port"],
                username=auth["user"],
                password=auth["pass"],
                database=auth["db"],
                ssl=auth["ssl"],
                timeout=1,
                retries=5,)
        except Exception as e:
            logging.error("Error connecting to InfluxDB: " + str(e))
            exit()

    def callback_sensor_publish(self, data):
        try:
            data = sensor_data_format(
                self.cache['SHORT_IDENT'],
                data.uid,
                str(data.value),
                {"type": data.brick_tag, }, )
            self.client.write_points([data])
            logging.debug("Published to influx", data)
        except Exception as e:
            logging.error("Error publishing to InfluxDB: " + str(e))
