#!/usr/bin/env python
#  Arup IoT Desk Controller
#  Ben Hussey <ben.hussey@arup.com> - March 2017

import sched
import time
from tinkerforge.ip_connection import IPConnection
from config import *
# import gettext
# gettext.install('deskcontrol', 'locale', unicode=1)


class Controller:
    identity = SHORT_IDENT

    ipcon = None
    current_module = None
    previous_module = None
    screen = None

    modules = {}
    ticklist = []

    # Event handlers handle internal events
    event_handlers = {}
    # The local database stores key value pairs
    localdb = None

    scheduler = sched.scheduler(time.time, time.sleep)

    def __init__(self):
        self.ipcon = IPConnection()
        self.ipcon.connect(HOST, PORT)

        for module in MODULES:
            self.add_module(module)

        if "MenuModule" in self.modules:
            for module in MENU_MODULES:
                self.add_module(module)
                self.modules["MenuModule"].add_menu_item(
                    self.modules[module[0]])

        self.ipcon.register_callback(
            IPConnection.CALLBACK_ENUMERATE, self.assign_bricklets)
        self.scheduler.enter(2, 1, self.ipcon.enumerate, (),)

    def add_module(self, module):
        self.modules[module[0]] = getattr(
            __import__("modules." + module[1],
                       fromlist=[module[0]]), module[0])(self)
        if self.modules[module[0]].always_tick:
            self.ticklist.append(module[0])
        print("Loaded " + module[0])

    def tick(self):
        if self.current_module:
            self.current_module.tick()
        for module in self.ticklist:
            self.modules[module].tick()
        self.scheduler.enter(1, 1, desk.tick, (),)

    def change_module(self, module):
        if not module:
            self.current_module = None
            if self.screen:
                self.screen.draw_splash()
        else:
            if self.current_module:
                self.previous_module = self.current_module
            if module in self.modules:
                # print("changing to " + module)
                self.current_module = self.modules[module]
            self.current_module.draw()

    def prev_module(self):
        if self.previous_module:
            self.change_module(self.previous_module.id)

    def navigate(self, direction):
        if "SleepModule" in self.modules:
            self.modules["SleepModule"].motion_changed(1)
        if direction not in ["forward", "back", "up", "down", "enter"]:
            return
        if self.current_module:
            self.current_module.navigate(direction)
        else:
            self.change_module("MenuModule")

    def assign_bricklets(
            self, uid, connected_uid, position, hardware_version,
            firmware_version, device_identifier, enumeration_type):
        if enumeration_type == IPConnection.ENUMERATION_TYPE_DISCONNECTED:
            return
        for state in self.modules:
            self.modules[state].try_bricklet(uid, device_identifier, position)

    def event(self, event, data):
        print("event triggered", str(event), str(data))
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                handler(data)

    def add_event_handler(self, event, handler):
        if event in self.event_handlers:
            self.event_handlers[event].append(handler)
        else:
            self.event_handlers[event] = [handler, ]


if __name__ == "__main__":
    try:
        desk = Controller()
        desk.tick()
        desk.scheduler.run()
    except KeyboardInterrupt:
        desk.ipcon.disconnect()
        print("Exiting")
