HOST = "localhost"
PORT = 4223

SHORT_IDENT = "XXXX"

INFLUX_AUTH = {
    "host": "127.0.0.1",
    "port": 8086,
    "user": "admin",
    "pass": "admin",
    "db": "iotdesks"
}

FIREBASE_AUTH = None

MODULES = [
    ("MenuModule", "navigation", "Navigation"),
    ("InputModule", "inputs", "Inputs"),
    ("SchedulerModule", "scheduler", "Schedule"),
    ("RFIDModule", "rfid", "RFID"),
    ("BrickModule", "brick", "Brick"),
    ("InfluxModule", "influx", "InfluxDB"),
    ("CommanderModule", "commander", "Commander"),
]

MENU_MODULES = [
    ("SensorModule", "sensors", "Sensors"),
    ("LightingModule", "lighting", "Lighting"),
    # ("PowerModule", "power", "Power"),
    ("NetworkModule", "network", "Network"),
]

try:
    config_module = __import__('config_local',
                               globals(), locals())

    print "config_module", config_module

    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)
except Exception:
    pass
