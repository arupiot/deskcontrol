import os

NAME_AUTHORITY = os.environ.get("NAME_AUTHORITY", "eightfitzroy.arupiot.com")
DEVICE_NAME = os.environ.get("DEVICE_NAME", "TST-1")

HOST = os.environ.get("BRICKD_HOST", "localhost")
PORT = int(os.environ.get("BRICKD_PORT", "4223"))

SHORT_IDENT = os.environ.get("SHORT_IDENT", "test")

MODULES = []
MENU_MODULES = []
MQTT_CONFIG = {}
ZMQ_CONFIG = {}
GCLOUD_CONFIG = {}
INFLUX_AUTH = {}

ENVAR_MODULES = {
    "ENABLE_MODULE_MENU": ("MenuModule", "navigation", "Navigation"),
    "ENABLE_MODULE_INPUT": ("InputModule", "inputs", "Inputs"),
    "ENABLE_MODULE_SLEEP": ("SleepModule", "sleep", "Sleep"),
    "ENABLE_MODULE_RFID": ("RFIDModule", "rfid", "RFID"),
    "ENABLE_MODULE_INFLUX": ("InfluxModule", "influx", "InfluxDB"),
    "ENABLE_MODULE_HTTP_PUSH": ("HttpPushModule", "httppush", "HTTPpush"),
    "ENABLE_MODULE_TF_SCREEN": ("TFScreen", "tfscreen", "TF Screen"),
    "ENABLE_MODULE_KIVY_SCREEN": ("KivyScreen", "kivyscreen", "Kivy Screen"),
    "ENABLE_MODULE_GOOGLE_IOT": ("GoogleIoTModule", "googleiot", "GoogleIoT"),
    "ENABLE_MODULE_MQTT": ("MQTTModule", "mqtt_module", "MQTT"),
    "ENABLE_MODULE_ZMQ": ("ZMQModule", "zmq_module", "ZMQ"),
    "ENABLE_MODULE_KILN": ("KilnModule", "kiln", "Kiln"),
    "ENABLE_MODULE_PICKLE": ("PickleModule", "pickle", "Local Storage"),
}

for envar in ENVAR_MODULES:
    if os.environ.get(envar):
        MODULES.append(ENVAR_MODULES[envar])

ENVAR_MENU_MODULES = {
    "ENABLE_MENU_SENSOR": ("SensorModule", "sensors", "Sensors"),
    "ENABLE_MENU_LIGHTING": ("LightingModule", "lighting", "Lighting"),
    "ENABLE_MENU_DC_POWER": ("DCPowerModule", "dcpower", "Power"),
    "ENABLE_MENU_AC_POWER": ("ACPowerModule", "acpower", "Power"), # Works on RPi only
    "ENABLE_MENU_NETWORK": ("NetworkModule", "network", "Network")
}

for envar in ENVAR_MENU_MODULES:
    if os.environ.get(envar):
        MODULES.append(ENVAR_MENU_MODULES[envar])

if os.environ.get("ENABLE_MODULE_INFLUX"):
    INFLUX_AUTH = {
        "host": os.environ.get("INFLUXDB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("INFLUXDB_PORT", "8086")),
        "user": os.environ.get("INFLUXDB_USER", "admin"),
        "pass": os.environ.get("INFLUXDB_PASS", "admin"),
        "db": os.environ.get("INFLUXDB_DB", "iotdesks"),
        "ssl": bool(os.environ.get("INFLUXDB_HOST"))
    }

if os.environ.get("ENABLE_MODULE_GOOGLE_IOT"):
    GCLOUD_CONFIG = {
        "project_id": os.environ.get("GCLOUD_PROJECT_ID", "digital-building-0000000000000"),
        "cloud_region": os.environ.get("GCLOUD_REGION", "europe-west1"),
        "registry_id": os.environ.get("GCLOUD_REGISTRY_ID", "iotdesks"),
        "device_id": os.environ.get("GCLOUD_DEVICE_ID", "XXXX"),
        "private_key_file": os.environ.get("GCLOUD_PRIVATE_KEY_FILE", "keys/rsa_private.pem"),
        "algorithm": os.environ.get("GCLOUD_ALGORITHM", "RS256"),
        "ca_certs": os.environ.get("GCLOUD_CA_CERTS", "keys/google.pem"),
        "mqtt_bridge_hostname": os.environ.get("GCLOUD_MQTT_HOST", "mqtt.googleapis.com"),
        "mqtt_bridge_port": int(os.environ.get("GCLOUD_MQTT_PORT", "8883")),
    }

if os.environ.get("ENABLE_MODULE_MQTT"):
    MQTT_CONFIG = {
        "mqtt_username": os.environ.get("MQTT_USERNAME"),
        "mqtt_password": os.environ.get("MQTT_PASSWORD"),
        "mqtt_client_id": os.environ.get("MQTT_CLIENT_ID", "test"),
        "mqtt_broker_host": os.environ.get("MQTT_BROKER_HOST"),
        "mqtt_broker_port": int(os.environ.get("MQTT_BROKER_PORT", "8883")),
        "mqtt_publish_topic": os.environ.get("MQTT_PUBLISH_TOPIC", "/ishiki/test/events"),
        "mqtt_subscribe_topic": os.environ.get("MQTT_SUBSCRIBE_TOPIC", "/ishiki/test/commands"),
    }

if os.environ.get("ENABLE_MODULE_ZMQ"):
    ZMQ_CONFIG = {
        "zmq_port": os.environ.get("ZMQ_PORT"),
        "zmq_topic": os.environ.get("ZMQ_TOPIC"),
    }

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
