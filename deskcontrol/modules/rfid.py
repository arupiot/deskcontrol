from tinkerforge.bricklet_nfc_rfid import BrickletNFCRFID
from navigation import StateModule


class RFIDModule(StateModule):
    readers = {}
    previous = None
    tick_count = 0
    tag_type = 0
    auth = "Nobody"

    users = {
        "411713624212177128": "Ben",
        "45014924212177128": "Mike",
        "41166424212177128": "Francesco",
    }

    def draw(self, clear=True):
        self.controller.screen.draw(
            "values",
            {"title": "Hello,", "value": self.auth, })

    def read_card(self, state, idle, nr):
        if idle:
            self.tag_type = (self.tag_type + 1) % 3
            nr.request_tag_id(self.tag_type)

        if state == nr.STATE_REQUEST_TAG_ID_READY:
            ret = nr.get_tag_id()
            card = str("".join(map(str, ret.tid[:ret.tid_length])))
            print(card)
            if card in self.users:
                self.auth = self.users[card]
            else:
                self.auth = "Unknown"
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
                lambda x, y: self.read_card(
                    x, y,
                    self.readers["card"]["instance"]))
            self.readers["card"]["instance"].request_tag_id(
                self.readers["card"]["instance"].TAG_TYPE_MIFARE_CLASSIC)
            # print("Created Card Reader")

    def navigate(self, direction):
        self.controller.change_module("MenuModule")

    def tick(self):
        self.tick_count += 1
        if self.tick_count > 5:
            self.controller.change_module("MenuModule")
