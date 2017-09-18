from datetime import datetime


def sensor_data(controller, key, value, tags={}):
    ident = controller.identity
    data = {
        "measurement": str(ident + "_" + key),
        "time": (
            datetime.utcnow().replace(microsecond=0).isoformat() +
            "Z"),
        "tags": tags,
        "fields": {"value": value, }
    }
    return data
