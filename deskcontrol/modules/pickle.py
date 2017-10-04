from navigation import StateModule
import pickledb
from config import PICKLEDB


class PickleModule(StateModule):
    client = None

    def __init__(self, controller):
        super(PickleModule, self).__init__(controller)
        self.db = pickledb.load(PICKLEDB, False)
        controller.localdb = self

    def get(self, key):
        return self.db.get(key)

    def set(self, key, value):
        return self.db.set(key, value)
