from iotnode.module import NodeModule

class menu_module(object):
    def __init__(self, title):
        self.title = title

    def __call__(self, module):
        
        return module


class MenuModule(NodeModule):
    items = []
    current = 0

    def __init__(self, *args, **kwargs):
        super(MenuModule, self).__init__(*args, **kwargs)
        self.push({"type": "input", "switch": "MenuModule"})

    def draw(self):
        if self.items:
            self.push({"type": "render_data", "data": {
                "title": self.items[self.current][1],
                "icon": self.items[self.current][1].lower()}})

    def callback_menu_add(self, data):
        self.items.append((data['_source'], data['title']))

    def callback_input(self, direction):
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
            # logging.debug("Menu: " + str(self.items[self.current][1]))
