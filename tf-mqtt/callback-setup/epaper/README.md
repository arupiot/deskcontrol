```
mosquitto_pub -t ishiki-mini/request/e_paper_296x128_bricklet/JAS/fill_display -m '{"color": "black"}'

then

mosquitto_pub -t ishiki-mini/request/e_paper_296x128_bricklet/JAS/draw_text -m '{"position_x": 16, "position_y": 48, "font": "12x16", "color": "white", "orientation": "horizontal", "text": "REACH FOR THE SKY"}'

then

mosquitto_pub -t ishiki-mini/request/e_paper_296x128_bricklet/JAS/draw -m ''

```