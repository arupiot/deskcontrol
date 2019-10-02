```
mosquitto_pub -t tinkerforge/register/accelerometer_v2_bricklet/HCV/acceleration -m '{"register":true}'

then

mosquitto_pub -t tinkerforge/request/accelerometer_v2_bricklet/HCV/set_acceleration_callback_configuration -m '{"period": 1000, "value_has_to_change": false}'
```