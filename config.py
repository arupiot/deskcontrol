# import gettext
# t = gettext.translation('deskcontrol', 'locale')
# _ = t.ugettext


def _(message):
    return message


HOST = "localhost"
PORT = 4223

SHORT_IDENT = "XXXX"

INFLUX_AUTH = {
    "host": "127.0.0.1",
    "port": 8086,
    "user": "admin",
    "pass": "admin",
    "db": "iotdesks"}

MODULES = [
    ("MenuModule", "navigation", _("Navigation")),
    ("InputModule", "inputs", _("Inputs")),
    ("SchedulerModule", "scheduler", _("Schedule")),
    ("RFIDModule", "rfid", _("RFID")),
    ("BrickModule", "brick", _("Brick")),
    ("InfluxModule", "influx", _("InfluxDB")),
    ("CommanderModule", "commander", _("Commander")),
    ("IdentityModule", "identity", _("Identity")),
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

try:
    config_module = __import__('config_local',
                               globals(), locals())

    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)
except Exception:
    pass
