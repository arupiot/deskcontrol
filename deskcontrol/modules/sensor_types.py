from tinkerforge.bricklet_temperature import BrickletTemperature
from tinkerforge.bricklet_temperature_ir import BrickletTemperatureIR
from tinkerforge.bricklet_uv_light import BrickletUVLight
from tinkerforge.bricklet_humidity import BrickletHumidity
from tinkerforge.bricklet_voltage_current import BrickletVoltageCurrent
from tinkerforge.bricklet_sound_intensity import BrickletSoundIntensity
from tinkerforge.bricklet_ambient_light_v2 import BrickletAmbientLightV2
from tinkerforge.bricklet_distance_ir import BrickletDistanceIR
from tinkerforge.bricklet_co2 import BrickletCO2
from tinkerforge.bricklet_color import BrickletColor
from tinkerforge.bricklet_barometer import BrickletBarometer
from tinkerforge.bricklet_line import BrickletLine
from tinkerforge.bricklet_hall_effect import BrickletHallEffect
from tinkerforge.bricklet_accelerometer import BrickletAccelerometer
from tinkerforge.bricklet_moisture import BrickletMoisture
from tinkerforge.bricklet_dual_relay import BrickletDualRelay
from tinkerforge.bricklet_motion_detector import BrickletMotionDetector
from tinkerforge.bricklet_rgb_led_button import BrickletRGBLEDButton
from tinkerforge.bricklet_dual_button import BrickletDualButton
from tinkerforge.bricklet_motion_detector_v2 import BrickletMotionDetectorV2
from tinkerforge.bricklet_rotary_poti import BrickletRotaryPoti
from tinkerforge.bricklet_tilt import BrickletTilt
from tinkerforge.bricklet_distance_us import BrickletDistanceUS
from tinkerforge.bricklet_rotary_encoder_v2 import BrickletRotaryEncoderV2
from tinkerforge.bricklet_linear_poti import BrickletLinearPoti
from tinkerforge.bricklet_thermal_imaging import BrickletThermalImaging
from tinkerforge.bricklet_line import BrickletLine

SENSORS = {
    "temp": {
        "name": "Temperature",
        "class": BrickletTemperature,
        "units": "degC",
        "brick_tag": "Temperature_Sensor",
        "value_func": "get_temperature",
        "multiplier": 0.01,
        "callback_func": "CALLBACK_TEMPERATURE",
        "variance": 1,
    },
    "ir_temp": {
        "name": "IR Temperature",
        "class": BrickletTemperatureIR,
        "units": "degC",
        "brick_tag": "IRTemperature_Sensor",
        "value_func": "get_object_temperature",
        "multiplier": 0.1,
        "callback_func": "CALLBACK_OBJECT_TEMPERATURE",
        "variance": 1,
    },
    "uv": {
        "name": "Ultraviolet",
        "class": BrickletUVLight,
        "units": "uW/cm2",
        "brick_tag": "UV_Light",
        "value_func": "get_uv_light",
    },
    "humidity": {
        "name": "Humidity",
        "class": BrickletHumidity,
        "units": "%RH",
        "brick_tag": "Humidity_Sensor",
        "value_func": "get_humidity",
        "multiplier": 0.1,
        "callback_func": "CALLBACK_HUMIDITY",
    },
    "light": {
        "name": "Ambient Light",
        "class": BrickletAmbientLightV2,
        "units": "lux",
        "brick_tag": "LightingSystem_Illuminance_Sensor",
        "value_func": "get_illuminance",
        "multiplier": 0.01,
        "callback_func": "CALLBACK_ILLUMINANCE",
    },
    "sound": {
        "name": "Sound Intensity",
        "class": BrickletSoundIntensity,
        "units": "",
        "brick_tag": "Noise_Sensor",
        "value_func": "get_intensity",
        "callback_func": "CALLBACK_INTENSITY",
        "publish_limit": 30,
        "variance": 400,
    },
    "co2": {
        "name": "Carbon Dioxide",
        "class": BrickletCO2,
        "units": "ppm",
        "brick_tag": "CO2_Sensor",
        "value_func": "get_co2_concentration",
        "callback_func": "CALLBACK_CO2_CONCENTRATION",
        "publish_limit": 10,
        "variance": 50,
    },
    "voltage": {
        "name": "Voltage",
        "class": BrickletVoltageCurrent,
        "units": "V",
        "brick_tag": "Electrical_Power_Meter",
        "value_func": "get_voltage",
        "multiplier": 0.001,
        "value_offset": 0,
        "callback_func": "CALLBACK_VOLTAGE",
    },
    "current": {
        "name": "Current",
        "class": BrickletVoltageCurrent,
        "units": "A",
        "brick_tag": "Electrical_Power_Meter",
        "value_func": "get_current",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_CURRENT",
    },
    "power": {
        "name": "Power",
        "class": BrickletVoltageCurrent,
        "units": "W",
        "brick_tag": "Electrical_Power_Meter",
        "value_func": "get_power",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_POWER",
    },
    "dist": {
        "name": "Desk Height",
        "class": BrickletDistanceIR,
        "units": "cm",
        "brick_tag": "Range_Sensor",
        "value_func": "get_distance",
        "multiplier": 0.1,
        "callback_func": "CALLBACK_DISTANCE",
    },
    "colour": {
        "name": "Colour",
        "class": BrickletColor,
        "units": "",
        "brick_tag": "Colour_Sensor",
        "value_func": "get_color",
        "callback_func": "CALLBACK_COLOR",
    },
    "colour_temp": {
        "name": "Colour Temp",
        "class": BrickletColor,
        "units": "K",
        "brick_tag": "Colour_Temperature_Sensor",
        "value_func": "get_color_temperature",
        "callback_func": "CALLBACK_COLOR_TEMPERATURE",
    },
    "air_pressure": {
        "name": "Air Pressure",
        "class": BrickletBarometer,
        "units": "mbar",
        "brick_tag": "Air_Pressure_Sensor",
        "value_func": "get_air_pressure",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_AIR_PRESSURE",
    },
    "reflectivity": {
        "name": "Reflectivity",
        "class": BrickletLine,
        "units": "",
        "brick_tag": "Line_Sensor",
        "value_func": "get_reflectivity",
        "callback_func": "CALLBACK_REFLECTIVITY",
    },
    "magfield": {
        "name": "Magn. Field",
        "class": BrickletHallEffect,
        "units": "",
        "brick_tag": "Magnetic_Field_Sensor",
        "value_func": "get_edge_count",
        "callback_func": "CALLBACK_EDGE_COUNT",
    },
    "acceleration": {
        "name": "Vibration",
        "class": BrickletAccelerometer,
        "units": "g",
        "brick_tag": "Accelerometer_Sensor",
        "value_func": "get_acceleration",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_ACCELERATION",
    },
    "acceleration_x": {
        "name": "Vibration X-Axis",
        "class": BrickletAccelerometer,
        "units": "g",
        "brick_tag": "Accelerometer_Sensor_X",
        "value_func": "get_acceleration",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_ACCELERATION",
    },
    "acceleration_y": {
        "name": "Vibration Y-Axis",
        "class": BrickletAccelerometer,
        "units": "g",
        "brick_tag": "Accelerometer_Sensor_Y",
        "value_func": "get_acceleration",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_ACCELERATION",
    },
    "acceleration_z": {
        "name": "Vibration Z-Axis",
        "class": BrickletAccelerometer,
        "units": "g",
        "brick_tag": "Accelerometer_Sensor_Z",
        "value_func": "get_acceleration",
        "multiplier": 0.001,
        "callback_func": "CALLBACK_ACCELERATION",
    },
    "moisture": {
        "name": "Moisture",
        "class": BrickletMoisture,
        "units": "",
        "brick_tag": "Moisture_Sensor",
        "value_func": "get_moisture_value",
        "callback_func": "CALLBACK_MOISTURE",
    },
    "dualrelay": {
        "name": "Dual Relay Bricklet",
        "class": BrickletDualRelay,
        "units": "",
        "brick_tag": "Relay_Sensor",
        "value_func": "get_state",
    },
    "motion": {
        "name": "Motion Detector",
        "class": BrickletMotionDetector,
        "units": "",
        "brick_tag": "Motion_Detector",
        "value_func": "get_motion_detected",
    },
    "button_colour": {
        "name": "RGB LED Button",
        "class": BrickletRGBLEDButton,
        "units": "",
        "brick_tag": "RGB_LED_Button",
        "value_func": "get_color",
    },
    "rgb_button_state": {
        "name": "RGB LED Button",
        "class": BrickletRGBLEDButton,
        "units": "",
        "brick_tag": "RGB_LED_Button",
        "value_func": "get_button_state()",
        "callback_func": "CALLBACK_BUTTON_STATE_CHANGED",
    },
    "left_button_state": {
        "name": "Dual Button",
        "class": BrickletDualButton,
        "units": "",
        "brick_tag": "Dual_Button_L",
        "value_func": "get_button_states",
        "callback_func": "CALLBACK_STATE_CHANGED",
    },
    "motion_2": {
        "name": "Motion Detector",
        "class": BrickletMotionDetectorV2,
        "units": "",
        "brick_tag": "Motion_Detector",
        "value_func": "get_motion_detected",
        "callback_func": "CALLBACK_MOTION_DETECTED",
    },
    "rotation_poti": {
        "name": "Rotary Poti",
        "class": BrickletRotaryPoti,
        "units": "",
        "brick_tag": "Rotary_Poti",
        "value_func": "get_position",
        "callback_func": "CALLBACK_POSITION",
    },
    "tilt": {
        "name": "Tilt",
        "class": BrickletTilt,
        "units": "",
        "brick_tag": "Tilt",
        "value_func": "get_tilt_state",
        "callback_func": "CALLBACK_TILT_STATE",
    },
	"dist_us": {
        "name": "Distance US",
        "class": BrickletDistanceUS,
        "units": "cm",
        "brick_tag": "Range_Sensor",
        "value_func": "get_distance_value",
        "multiplier": 0.1,
        "callback_func": "CALLBACK_DISTANCE",
    },
	"rotation_encoder": {
        "name": "Rotary Encoder",
        "class": BrickletRotaryEncoderV2,
        "units": "",
        "brick_tag": "Rotary_Encoder",
        "value_func": "get_count",
        "callback_func": "CALLBACK_COUNT",
    },
	"linear": {
		    "name": "Linear Poti",
		    "class": BrickletLinearPoti,
		    "units": "",
		    "brick_tag": "Linear_Poti",
		    "value_func": "get_position",
		    "callback_func": "CALLBACK_POSITION",
	},
	"thermal_image": {
		    "name": "Thermal Imaging",
		    "class": BrickletThermalImaging,
		    "units": "K",
		    "multiplier": 0.01,
		    "brick_tag": "Thermal_Imaging",
		    "value_func": "get_statistics",
	},
	"reflectivity": {
		    "name": "Line",
		    "class": BrickletLine,
		    "units": "",
		    "brick_tag": "Line",
		    "value_func": "get_reflectivity",
		    "callback_func": "CALLBACK_REFLECTIVITY",
	},
}
