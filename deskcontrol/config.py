import os

NAME_AUTHORITY = os.environ.get("NAME_AUTHORITY", "eightfitzroy.arupiot.com")
DEVICE_NAME = os.environ.get("DEVICE_NAME", "TST-1")

HOST = os.environ.get("BRICKD_HOST", "localhost")
PORT = int(os.environ.get("BRICKD_PORT", "4223"))

SHORT_IDENT = os.environ.get("SHORT_IDENT", "test")

MODULES = [
    # ("MenuModule", "navigation", "Navigation"),
    # ("InputModule", "inputs", "Inputs"),
    # ("SleepModule", "sleep", "Sleep"),
    # ("RFIDModule", "rfid", "RFID"),
    # ("InfluxModule", "influx", "InfluxDB"),
    # ("HttpPushModule", "httppush", "HTTPpush"),
    # ("TFScreen", "tfscreen", "TF Screen"),
    # ("KivyScreen", "kivyscreen", "Kivy Screen"),
    # ("GoogleIoTModule", "googleiot", "GoogleIoT"),
    # ("KilnModule", "kiln", "Kiln"),
    # ("PickleModule", "pickle", "Local Storage"),
]

MENU_MODULES = [
    # ("SensorModule", "sensors", "Sensors"),
    # ("LightingModule", "lighting", "Lighting"),
    # ("DCPowerModule", "dcpower", "Power"),
    # ("ACPowerModule", "acpower", "Power"),  # Works on RPi only
    # ("NetworkModule", "network", "Network"),
]

MQTT_CONFIG = {}
ZMQ_CONFIG = {}
GCLOUD_CONFIG = {}
INFLUX_AUTH = {}


if os.environ.get("ENABLE_MODULE_MENU"):
    MODULES.append(("MenuModule", "navigation", "Navigation"))

if os.environ.get("ENABLE_MODULE_INPUT"):
    MODULES.append(("InputModule", "inputs", "Inputs"))

if os.environ.get("ENABLE_MODULE_SLEEP"):
    MODULES.append(("SleepModule", "sleep", "Sleep"))

if os.environ.get("ENABLE_MODULE_RFID"):
    MODULES.append(("RFIDModule", "rfid", "RFID"))

if os.environ.get("ENABLE_MODULE_INFLUX"):
    MODULES.append(("InfluxModule", "influx", "InfluxDB"))

    INFLUX_AUTH = {
        "host": os.environ.get("INFLUXDB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("INFLUXDB_PORT", "8086")),
        "user": os.environ.get("INFLUXDB_USER", "admin"),
        "pass": os.environ.get("INFLUXDB_PASS", "admin"),
        "db": os.environ.get("INFLUXDB_DB", "iotdesks"),
        "ssl": bool(os.environ.get("INFLUXDB_HOST"))
    }

if os.environ.get("ENABLE_MODULE_HTTP_PUSH"):
    MODULES.append(("HttpPushModule", "httppush", "HTTPpush"))

if os.environ.get("ENABLE_MODULE_TF_SCREEN"):
    MODULES.append(("TFScreen", "tfscreen", "TF Screen"))

if os.environ.get("ENABLE_MODULE_KIVY_SCREEN"):
    MODULES.append(("KivyScreen", "kivyscreen", "Kivy Screen"))

if os.environ.get("ENABLE_MODULE_GOOGLE_IOT"):
    MODULES.append(("GoogleIoTModule", "googleiot", "GoogleIoT"))

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
    MODULES.append(("MQTTModule", "mqtt_module", "MQTT"))

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
    MODULES.append(("ZMQModule", "zmq_module", "ZMQ"))

    ZMQ_CONFIG = {
        "zmq_port": os.environ.get("ZMQ_PORT"),
        "zmq_topic": os.environ.get("ZMQ_TOPIC"),
    }


if os.environ.get("ENABLE_MODULE_KILN"):
    MODULES.append(("KilnModule", "kiln", "Kiln"))

if os.environ.get("ENABLE_MODULE_PICKLE"):
    MODULES.append(("PickleModule", "pickle", "Local Storage"))

##############################  MENUS  ########################################

if os.environ.get("ENABLE_MENU_SENSOR"):
    MENU_MODULES.append(("SensorModule", "sensors", "Sensors"))

if os.environ.get("ENABLE_MENU_LIGHTING"):
    MENU_MODULES.append(("LightingModule", "lighting", "Lighting"))

if os.environ.get("ENABLE_MENU_DC_POWER"):
    MENU_MODULES.append(("DCPowerModule", "dcpower", "Power"))

if os.environ.get("ENABLE_MENU_AC_POWER"): # Works on RPi only
    MENU_MODULES.append(("ACPowerModule", "acpower", "Power"))

if os.environ.get("ENABLE_MENU_NETWORK"):
    MENU_MODULES.append(("NetworkModule", "network", "Network"))


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
