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
    ("SchedulerModule", "scheduler", "Schedule"),
    ("RFIDModule", "rfid", "RFID"),
    ("BrickModule", "brick", "Brick"),
    ("InfluxModule", "influx", "InfluxDB"),
    ("GoogleIoTModule", "googleiot", "GoogleIoT"),
    ("CommanderModule", "commander", "Commander"),
]

MENU_MODULES = [
    ("SensorModule", "sensors", "Sensors"),
    ("LightingModule", "lighting", "Lighting"),
    # ("PowerModule", "power", "Power"),
    ("NetworkModule", "network", "Network"),
]

SCHEMA_POST_URL = ""

try:
    config_module = __import__('config_local',
                               globals(), locals())

    for setting in dir(config_module):
        if setting == setting.upper():
            locals()[setting] = getattr(config_module, setting)
except Exception:
    pass
