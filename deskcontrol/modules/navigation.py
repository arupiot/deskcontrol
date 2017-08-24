from screen import Screen


class StateModule(object):
    always_tick = False

    def __init__(self, controller):
        self.id = self.__class__.__name__
        self.controller = controller

    def draw(self):
        pass

    def try_bricklet(self, uid, device_identifier, position):
        pass

    def navigate(self, direction):
        pass

    def tick(self):
        return


class MenuModule(StateModule):
    items = []
    current = 0

    def draw(self, clear=True):
        self.controller.screen.draw(
            "menu",
            {"title": self.items[self.current][1],
             "icon": self.items[self.current][1].lower()})
        #    if clear:
        #        self.controller.screen.clear_display()
        #    pos = 0
        #    start = max(0, min(self.current - 2, len(self.items) - 5))
        #    while pos < min(5, len(self.items)):
        #        self.controller.screen.write_line(pos+2, 0,
        #            "  " + self.items[start+pos][1])
        #        self.controller.screen.write_line(pos+2, 23, " ")
        #        pos = pos + 1
        #    cursor = min(start+self.current, max(
        #                 min(self.current, 2),
        #                 self.current + 5 - len(self.items)))
        #    self.controller.screen.write_line(cursor+2, 23, ">")

    def add_menu_item(self, module):
        self.items.append((module.id, module.menu_title))

    def try_bricklet(self, uid, device_identifier, position):
        if not self.controller.screen:
            if device_identifier == 263:
                self.controller.screen = Screen(self.controller, uid)
                print("Screen Initialised")
                return True
            return False

    def navigate(self, direction):
        if direction == "forward":
            self.controller.change_module(self.items[self.current][0])
        if direction == "back":
            self.controller.screen.draw_splash()
            self.controller.current_module = None
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.items):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.items) - 1
            self.draw(clear=False)
            print("Menu: " + str(self.items[self.current][1]))
