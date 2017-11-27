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

    def add_menu_item(self, module):
        self.items.append((module.id, module.menu_title))

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
            # print("Menu: " + str(self.items[self.current][1]))
