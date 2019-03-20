from iotnode.module import NodeModule


class MenuModule(NodeModule):
    items = []
    current = 0
    splash = True

    def __init__(self, *args, **kwargs):
        super(MenuModule, self).__init__(*args, **kwargs)
        self.push({"type": "input", "switch": "MenuModule"})

    def draw(self):
        if self.splash:
            self.push({"type": "render_splash", })
        elif self.items:
            self.push({"type": "render_data", "data": {
                "title": self.items[self.current][1],
                "icon": self.items[self.current][1].lower()}})

    def callback_menu_add(self, data):
        self.items.append((data['_source'], data['title']))
        self.update()

    def callback_sleep(self, data):
        if 'sleep' in data:
            self.splash = True

    def callback_input(self, direction):
        if direction == "forward":
            if self.splash:
                self.splash = False
            else:
                self.push(
                    {"type": "input", "switch": self.items[self.current][0]})
        if direction == "back":
            self.splash = True
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.items):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.items) - 1
        self.update()
