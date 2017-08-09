from navigation import StateModule
import socket


def get_ip_address():
    try:
        return(socket.gethostbyname(socket.gethostname()))
    except Exception:
        return "No connection"


class NetworkModule(StateModule):
    menu_title = "Network"
    ip = None

    def draw(self, clear=True):
        self.ip = get_ip_address()  # get_ip_address("wlan0")
        if clear:
            self.controller.screen.device.clear_display()
        self.controller.screen.draw(
            "values",
            {"title": "IP Address", "value": str(self.ip), })

    def navigate(self, direction):
        self.controller.prev_module()
