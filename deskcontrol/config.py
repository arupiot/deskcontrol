HOST = "localhost"
PORT = 4223

SHORT_IDENT = "XXXX"

INFLUX_AUTH = {
    "host": "127.0.0.1",
    "port": 8086,
    "user": "admin",
    "pass": "admin",
    "db": "iotdesks",
    "ssl": False,
}

GCLOUD_CONFIG = {
    "project_id": "digital-building-0000000000000",
    "cloud_region": "europe-west1",
    "registry_id": "iotdesks",
    "device_id": "XXXX",
    "private_key_file": "keys/rsa_private.pem",
    "algorithm": "RS256",
    "ca_certs": "keys/google.pem",
    "mqtt_bridge_hostname": "mqtt.googleapis.com",
    "mqtt_bridge_port": 8883,
}

MODULES = [
    ("MenuModule", "navigation", "Navigation"),
    ("InputModule", "inputs", "Inputs"),
    ("SleepModule", "sleep", "Sleep"),
    ("RFIDModule", "rfid", "RFID"),
    ("InfluxModule", "influx", "InfluxDB"),
    ("HttpPushModule", "httppush", "HTTPpush"),
    ("TFScreen", "tfscreen", "TF Screen"),
    # ("KivyScreen", "kivyscreen", "Kivy Screen"),
    # ("GoogleIoTModule", "googleiot", "GoogleIoT"),
    # ("KilnModule", "kiln", "Kiln"),
    # ("PickleModule", "pickle", "Local Storage"),
]

MENU_MODULES = [
    ("SensorModule", "sensors", "Sensors"),
    # ("LightingModule", "lighting", "Lighting"),
    # ("DCPowerModule", "dcpower", "Power"),
    # ("ACPowerModule", "acpower", "Power"),  # Works on RPi only
    ("NetworkModule", "network", "Network"),
]

SCHEMA_POST_URL = ""
PICKLEDB = "deskcontrol.db"

try:
    config_module = __import__('config_local',
                               globals(), locals())

    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)
except Exception:
    pass
