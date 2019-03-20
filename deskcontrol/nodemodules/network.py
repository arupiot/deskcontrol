from iotnode.module import NodeModule
import netifaces as ni
import subprocess
import logging


def get_git_revision_short_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
    except Exception as e:
        logging.exception("Error Getting Get Revision")
        return None


def get_eth_address(iface="eth0"):
    try:
        ni.ifaddresses(iface)
        return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
    except Exception as e:
        logging.exception("Error Getting IP Address")
        return None


def get_wlan_address(iface="wlan0"):
    try:
        ni.ifaddresses(iface)
        return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
    except Exception as e:
        logging.exception("Error Getting IP Address")
        return None


def git_update():
    subprocess.check_output(["git", "pull", "--all"])
    subprocess.check_output(["sudo", "service", "deskcontrol", "restart"])


def reboot_pi():
    subprocess.check_output(["sudo", "reboot"])


class NetworkModule(NodeModule):
    current = 0
    triggered = False
    menu = {
        0: {
            "title": "Wireless IP",
            "get_value": get_wlan_address,
        },
        1: {
            "title": "Ethernet IP",
            "get_value": get_eth_address,
        },
        2: {
            "title": "Code Version",
            "get_value": get_git_revision_short_hash,
            "trigger": git_update,
        },
        3: {
            "title": "Reboot?",
            "value": "",
            "trigger": reboot_pi,
        },
    }

    def __init__(self, *args, **kwargs):
        super(NetworkModule, self).__init__(*args, **kwargs)
        self.add_to_menu("Network")

    def draw(self):
        key = self.menu.keys()[self.current]
        menu = self.menu[key]
        if "get_value" in menu:
            value = menu["get_value"]()
        else:
            value = menu["value"]
        self.push({"type": "render_data", "data": {
            "title": menu["title"], "data": str(value).rstrip(), }})

    def trigger(self):
        key = self.menu.keys()[self.current]
        menu = self.menu[key]
        if "trigger" in menu:
            self.triggered = True
            self.push({"type": "render_data", "data": {
                "values": {"title": menu["title"], "value": "Wait...", }}})
            menu["trigger"]()

    def callback_input(self, data):
        direction = data["data"]
        if self.triggered:
            return
        if direction in ["back", "left"]:
            self.push({"type": "input", "switch": "MenuModule"})
        if direction in ["enter", "right"]:
            self.trigger()
            self.draw()
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.menu):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.menu) - 1
            self.draw()
