from modules.navigation import StateModule
import netifaces as ni
import subprocess


def get_git_revision_short_hash():
    try:
        return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])
    except Exception as e:
        print("Error Getting Get Revision:")
        print(e)
        return None


def get_eth_address(iface="eth0"):
    try:
        ni.ifaddresses(iface)
        return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
    except Exception as e:
        print("Error Getting IP Address:")
        print(e)
        return None


def get_wlan_address(iface="wlan0"):
    try:
        ni.ifaddresses(iface)
        return ni.ifaddresses(iface)[ni.AF_INET][0]['addr']
    except Exception as e:
        print("Error Getting IP Address:")
        print(e)
        return None


def git_update():
    subprocess.check_output(["git", "pull", "--all"])
    subprocess.check_output(["sudo", "service", "deskcontrol", "restart"])


def reboot_pi():
    subprocess.check_output(["sudo", "reboot"])


class NetworkModule(StateModule):
    menu_title = "Network"
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

    def draw(self, clear=True):
        key = self.menu.keys()[self.current]
        menu = self.menu[key]
        if "get_value" in menu:
            value = menu["get_value"]()
        else:
            value = menu["value"]
        if clear:
            self.controller.screen.device.clear_display()
        self.controller.screen.draw(
            "values",
            {"title": menu["title"], "value": str(value).rstrip(), })

    def trigger(self):
        key = self.menu.keys()[self.current]
        menu = self.menu[key]
        if "trigger" in menu:
            self.triggered = True
            self.controller.screen.draw(
                "values",
                {"title": menu["title"], "value": "Please wait...", })
            menu["trigger"]()

    def navigate(self, direction):
        if self.triggered:
            return
        if direction == "back":
            self.controller.prev_module()
        if direction == "forward":
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
            # print("Output: " + str(list(self.outputs)[self.current]))
            self.draw()
