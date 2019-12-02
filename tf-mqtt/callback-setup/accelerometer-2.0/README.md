```
mosquitto_pub -t ishiki-mini/register/accelerometer_v2_bricklet/HCV/acceleration -m '{"register":true}'

then

mosquitto_pub -t ishiki-mini/request/accelerometer_v2_bricklet/HCV/set_acceleration_callback_configuration -m '{"period": 1000, "value_has_to_change": false}'
```