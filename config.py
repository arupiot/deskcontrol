# import gettext
# t = gettext.translation('deskcontrol', 'locale')
# _ = t.ugettext


def _(message):
    return message


# Host where brickd is running
HOST = "brickd"
PORT = 4223

DESK_ID = "A"

MODULES = [
    ("MenuModule", "navigation", _("Navigation")),
    ("InputModule", "inputs", _("Inputs")),
    ("SchedulerModule", "scheduler", _("Schedule")),
    ("RFIDModule", "rfid", _("RFID")),
    ("BrickModule", "brick", _("Brick")),
    ("IdentityModule", "identity", _("Identity")),
    ("InfluxModule", "influx", _("InfluxDB")),
]

MENU_MODULES = [
    ("SensorModule", "sensors", _("Sensors")),
    ("LightingModule", "lighting", _("Lighting")),
    ("PowerModule", "power", _("Power")),
    ("NetworkModule", "network", _("Network")),
]

VA_POSITIONS = {
    'a': _("Laptop Charger Power"),
    'b': _("Monitor Power"),
    'c': _("USB Outlets"),
    'd': _("Lighting Power"),
}

RELAY_POSITIONS = {
    'a': (_("Laptop Charger"), _("Monitor")),
    'b': (_("USB Outlets"), _("Lighting")),
}
