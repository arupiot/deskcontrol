```
mosquitto_pub -t tinkerforge/request/e_paper_296x128_bricklet/JAS/fill_display -m '{"color": "black"}'

then

mosquitto_pub -t tinkerforge/request/e_paper_296x128_bricklet/JAS/draw_text -m '{"position_x": 16, "position_y": 48, "font": "12x16", "color": "white", "orientation": "horizontal", "text": "REACH FOR THE SKY"}'

then

mosquitto_pub -t tinkerforge/request/e_paper_296x128_bricklet/JAS/draw -m ''

```


A note on installing PIL:

https://stackoverflow.com/questions/20060096/installing-pil-with-pip