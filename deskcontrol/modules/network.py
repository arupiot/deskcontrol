from navigation import StateModule
import netifaces as ni

def get_ip_address(iface):
    ni.ifaddresses(iface)
    return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']


class NetworkModule(StateModule):
    menu_title = "Network"
    ip = None

    def draw(self, clear=True):
        try:
            self.ip = get_ip_address("wlan0")
        except Exception:
            self.ip = None
        if clear:
            self.controller.screen.device.clear_display()
        self.controller.screen.draw(
            "values",
            {"title": "Wireless IP", "value": str(self.ip), })

    def navigate(self, direction):
        self.controller.prev_module()
