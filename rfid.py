from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
from navigation import StateModule

class RFIDModule(StateModule):
    name = "rfid"
    controller = None
    readers = {}
    previous = None
    tick_count = 0
    tag_type = 0

    def __init__(self, controller):
        self.controller = controller
        super(RFIDModule, self).__init__(controller)
        print "Created RFIDModule"

    def draw(self, clear=True):
        self.controller.screen.draw("values",
            {"title": "Hello,", "value": "     User!",})

    def read_card(self, state, idle, nr):
        if idle:
            self.tag_type = (self.tag_type + 1) % 3
            nr.request_tag_id(self.tag_type)

        if state == nr.STATE_REQUEST_TAG_ID_READY:
            ret = nr.get_tag_id()
            print("Found tag of type " + str(ret.tag_type) + " with ID [" +
                  " ".join(map(str, map(hex, ret.tid[:ret.tid_length]))) + "]")
            if (not self.previous and self.controller.current_module and
                self.controller.current_module.id != "RFIDModule"):
                self.previous = self.controller.current_module.id
            self.controller.change_module("RFIDModule")

    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 246:
            self.readers["card"] = {
                "instance": BrickletNFCRFID(uid, self.controller.ipcon),
                "name": "card",
                "relay": 0,
            }
            self.readers["card"]["instance"].register_callback(
                self.readers["card"]["instance"].CALLBACK_STATE_CHANGED,
                lambda x, y: self.read_card(x, y,
                    self.readers["card"]["instance"]))
            self.readers["card"]["instance"].request_tag_id(
                self.readers["card"]["instance"].TAG_TYPE_MIFARE_CLASSIC)
            print "Created Card Reader"


    def navigate(self, direction):
        if self.previous:
            self.controller.change_module(self.previous)
        else:
            self.controller.change_module("MenuModule")

    def tick(self):
        self.tick_count += 1
        if self.tick_count > 5:
            if self.previous:
                self.controller.change_module(self.previous)
            else:
                self.controller.change_module("MenuModule")
