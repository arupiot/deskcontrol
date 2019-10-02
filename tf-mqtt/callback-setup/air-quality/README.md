```
mosquitto_pub -t tinkerforge/register/air_quality_bricklet/JyW/all_values -m '{"register":true}'

then

mosquitto_pub -t tinkerforge/request/air_quality_bricklet/JyW/set_all_values_callback_configuration -m '{"period": 1000, "value_has_to_change": false}'
```