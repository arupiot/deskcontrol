from iotnode.module import NodeModule


class KivyScreen(NodeModule):

    def draw_splash(self):
        pass

    def callback_sleep(self, data):
        if 'sleep' in data:
            pass
        if 'wake' in data:
            pass

    def draw(self, layout, params):
        # layout will be menu, values or edit
        # params will be a dict with title, value, icon
        # see tfscreen.py for previous implementation
        pass
