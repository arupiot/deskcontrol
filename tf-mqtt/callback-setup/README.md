# Tinkerforge MQTT Bindings

https://www.tinkerforge.com/en/doc/Software/API_Bindings_MQTT.html#api-bindings-mqtt

## General steps

The MQTT binding API is _not_ a push button setup. That would result in a wealth! of data being pushed instantly. This is not desired. Set up the MQTT feed of each Tinkerforge device as below:

- Start the mqtt bindings with:

```
sudo python3 tinkerforge_mqtt --debug --broker-host $BROKER_IP
```

- mqtt bindings to a broker with tls (with much debug messaging and insecurity, not for production!)

```
python3 tinkerforge_mqtt --debug --broker-tls-insecure --broker-host $BROKER_IP --broker-certificate $CERT_PATH --broker-port 8080 --global-topic-prefix ishiki-mini/
```

(debug is optional, of course)

There are as many options as you'd expect from an MQTT client, see `python3 tinkerforge_mqtt --help` for more

- Find UID of bricklet

```
- Use a script
- Have a look in brickv
- e.g. the UID is JyW

```

- Register the callback

```
e.g. for the air quality bricklet

mosquitto_pub -t tinkerforge/register/air_quality_bricklet/JyW/all_values -m '{"register":true}'

```

- Set up the callback

```
mosquitto_pub -t tinkerforge/request/air_quality_bricklet/JyW/set_all_values_callback_configuration -m '{"period": 1000, "value_has_to_change": false}'
```

- Subscribe to the topic + visualise + do whatever you have to do

Each directory here has some sample `mosquitto_pub` and `mosquitto_sub` commands. They're directly pulled/modified from the  API docs in the link at the top of this readme 