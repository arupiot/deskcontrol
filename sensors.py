from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
from tinkerforge.bricklet_humidity import BrickletHumidity
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from tinkerforge.bricklet_co2 import BrickletCO2
from navigation import StateModule
from config import VA_POSITIONS
from screen import draw_image

class SensorModule(StateModule):
    name = "Sensor Values"
    controller = None
    sensors = {}
    current = 0

    def __init__(self, controller):
        self.controller = controller
        super(SensorModule, self).__init__(controller)
        print "Created SensorModule"


    def draw(self, clear=True):
        if clear:
            self.controller.screen.clear_display()
        if not len(self.sensors):
            self.controller.ipcon.enumerate()
            draw_image(self.controller, "NotConnected")
            return
        sensor = self.sensors[self.sensors.keys()[self.current]]
        if sensor["type"] == "temperature":
            if clear: draw_image(self.controller, sensor["type"])
            self.controller.screen.write_line(4, 8,
                str(sensor["instance"].get_temperature()/100.0) + " degC"
                )
        if sensor["type"] == "irtemp":
            if clear: draw_image(self.controller, sensor["type"])
            self.controller.screen.write_line(4, 8,
                str(sensor["instance"].get_ambient_temperature()/10.0) +
                " degC"
                )
        if sensor["type"] == "humidity":
            if clear: draw_image(self.controller, sensor["type"])
            self.controller.screen.write_line(4, 8,
                str(sensor["instance"].get_humidity()/10.0) + " %RH"
                )
        if sensor["type"] == "sound":
            if clear: draw_image(self.controller, sensor["type"])
            self.controller.screen.write_line(4, 8,
                str(sensor["instance"].get_intensity())
                )
        if sensor["type"] == "co2":
            if clear: draw_image(self.controller, sensor["type"])
            self.controller.screen.write_line(4, 8,
                str(sensor["instance"].get_co2_concentration()) + " ppm"
                )
        if sensor["type"] == "light":
            if clear: draw_image(self.controller, sensor["type"])
            self.controller.screen.write_line(4, 8,
                str(sensor["instance"].get_illuminance()/100) + " lux"
                )
        if sensor["type"] == "power":
            if clear: draw_image(self.controller, sensor["type"])
            volts = sensor["instance"].get_voltage()/1000
            current = sensor["instance"].get_current()/1000
            power = volts * current
            self.controller.screen.write_line(4, 0, "    " +
                str(volts) + " V"
                )
            self.controller.screen.write_line(5, 0, "    " +
                str(current) + " A"
                )
            self.controller.screen.write_line(6, 0, "    " +
                str(power) + " W"
                )


    def try_bricklet(self, uid, device_identifier, position):
        if device_identifier == 216:
            self.sensors["temp"] = {
                "instance": BrickletTemperature(uid, self.controller.ipcon),
                "name": "Temperature",
                "type": "temperature",
            }
            #  print "Created Temperature Sensor"
        elif device_identifier == 217:
            self.sensors["irtemp"] = {
                "instance": BrickletTemperatureIR(uid, self.controller.ipcon),
                "name": "IR Temperature",
                "type": "irtemp",
            }
            #  print "Created IR Temperature Sensor"
        elif device_identifier == 27:
            self.sensors["hum"] = {
                "instance": BrickletHumidity(uid, self.controller.ipcon),
                "name": "Humidity",
                "type": "humidity",
            }
            #  print "Created Humidity Sensor"
        elif device_identifier == 259:
            self.sensors["light"] = {
                "instance": BrickletAmbientLightV2(uid, self.controller.ipcon),
                "name": "Ambient Light",
                "type": "light",
            }
            #  print "Created Ambient Light Sensor"
        elif device_identifier == 238:
            self.sensors["sound"] = {
                "instance": BrickletSoundIntensity(uid, self.controller.ipcon),
                "name": "Sound Intensity",
                "type": "sound",
            }
            #  print "Created Sound Intensity Sensor"
        elif device_identifier == 262:
            self.sensors["co2"] = {
                "instance": BrickletCO2(uid, self.controller.ipcon),
                "name": "Carbon Dioxide",
                "type": "co2",
            }
            #  print "Created CO2 Sensor"
        elif device_identifier == 227:
            self.sensors["va"+position] = {
                "instance": BrickletVoltageCurrent(uid, self.controller.ipcon),
                "name": VA_POSITIONS[position],
                "type": "power",
            }
            #  print "Created Power Sensor"


    def navigate(self, direction):
        if direction == "back":
            self.controller.prev_module()
        if direction in ["down", "up"]:
            if direction == "down":
                self.current = self.current + 1
            else:
                self.current = self.current - 1
            if self.current >= len(self.sensors):
                self.current = 0
            elif self.current < 0:
                self.current = len(self.sensors)-1
            print "Sensor: " + str(list(self.sensors)[self.current])
            self.draw()


    def tick(self):
        self.draw(clear=False)
