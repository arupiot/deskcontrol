from navigation import StateModule
import socket
import fcntl
import struct


def get_ip_address(ifname):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
    except Exception:
        return "No wlan0"

def get_ip_address():
    try:
        return(socket.gethostbyname(socket.gethostname()))
    except Exception:
        return "No connection"

class NetworkModule(StateModule):
    name = "network"
    controller = None
    ip = None

    def __init__(self, controller):
        self.controller = controller
        super(NetworkModule, self).__init__(controller)

    def draw(self, clear=True):
        self.ip = get_ip_address() #get_ip_address("wlan0")
        if clear:
            self.controller.screen.device.clear_display()
        self.controller.screen.draw(
            "values",
            {"title": "IP Address", "value": str(self.ip), })

    def navigate(self, direction):
        self.controller.prev_module()
