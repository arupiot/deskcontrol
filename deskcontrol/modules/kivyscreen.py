class KivyScreen():
    controller = None
    device = None

    def __init__(self, controller):
        super(KivyScreen, self).__init__(controller)
        self.controller.screen = self
        controller.add_event_handler("sleep", self.on_sleep)
        controller.add_event_handler("wake", self.on_wake)

    def draw_splash(self):
        pass

    def on_sleep(self, data):
        pass

    def on_wake(self, data):
        pass

    def draw(self, layout, params):
        # layout will be menu, values or edit
        # params will be a dict with title, value, icon
        # see tfscreen.py for previous implementation
        pass
