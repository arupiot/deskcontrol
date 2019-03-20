from datetime import datetime, timedelta


def seconds_past(datetime, seconds):
    return (datetime < datetime.now() - timedelta(seconds=seconds))


def sensor_data_format(ident, key, value, tags={}):
    data = {
        "measurement": str(ident + "_" + key),
        "time": (
            datetime.utcnow().replace(microsecond=0).isoformat() +
            "Z"),
        "tags": tags,
        "fields": {"value": value, }
    }
    return data
