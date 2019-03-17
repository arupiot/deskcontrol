from iotnode.module import NodeModule
from tinkerforge.ip_connection import IPConnection
import logging


class TinkerForgeModule(NodeModule):
    bricklets = {}

    def __init__(self, *args, **kwargs):
        super(TinkerForgeModule, self).__init__(*args, **kwargs)

        if not "_TINKERFORGE" in self.cache:
            logging.error("No tinkerforge configuration found")
            exit()
        self.ipcon = IPConnection()
        self.ipcon.connect(
            self.cache["_TINKERFORGE"][0], self.cache["_TINKERFORGE"][1])

        self.ipcon.register_callback(
            IPConnection.CALLBACK_ENUMERATE, self.assign_bricklets)

    def assign_bricklets(
            self, uid, connected_uid, position, hardware_version,
            firmware_version, device_identifier, enumeration_type):
        if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
            return
        self.try_bricklet(uid, device_identifier, position)
