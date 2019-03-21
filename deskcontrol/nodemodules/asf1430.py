from iotnode.module import NodeModule
from classes.sensor import Sensor
from math import floor, log10
import serial
import binascii
import logging

'''
Sensirion ASF1430 Bidirectional Mass Flow Meter basic data parser
https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/0_Datasheets/Mass_Flow_Meter/Sensirion_Mass_Flow_Meters_ASF1430_Datasheet.pdf
James Hare <james.hare@arup.com> - March 2019

communicate to sensor using RS-232 19200/8/1
send 0x67,0x6f,0x0d ('go'+ carriage return) to sensor to start continuous measurements
send 0x73, 0x0d ('s'+ carriage return) to sensor to stop measurements
note that sending 'go' and 's' commands to sensor involves EEPROM read/write - limits lifespan
sensor retains status in non volatile memory. If 'go' sent previously, sensor will automatically send data on power on
recommended to simply read data from device, not send 'go' each time program is started
programmable resolution available - affects signal integration time in ms. Sending 'res=x' (ascii) where x is 0 to 7
sensor set to max res of 15 bit (x=7) for highest sensitivity. However means slowest data rate of 1.56 Hz (data sent every 640 ms)
sensor sends data in 4 byte packet. First two bytes 0x7F, 0x7F are sync bytes. Next two bytes are mass flow MSB & LSB as 16 bit signed int
scale factor of 70 used. Value therefore divided by 70
sensor uses sccm unit (standard cubic centimeter per minute). 1 sccm = 1 cm3/min = 1 ml/min at 0degC and 1013mbar pressure
sensor is bi-directional. Peak value is +-440 ml/min
resolution is 0.0143 ml/min
as sensor uses an internal heating resistor to measure gas flow by heating transfer, recommended to let sensor 'warm up'. No idea for how long
sensor has built in temperature compensation. Possible to read out temperature but have to switch modes from flow to temperature. Can't read both simultaneously.
sensor updates temperature compensation every minute. When it is reading temp, it can't read the flow at that exact moment in time
sensor appears to show a bit of jitter/zero error, even when plastic end caps are on and unit sealed. Sensor reads -17 when no flow (error of -0.243 ml/min)
I've put in a zero offset to try and correct for this. However picking up the sensor and moving it even when plugged causes jitter.
Zero offset therefore needs playing around with when installed
Potential to incorporate averaging over a time period. 10 seconds / 30 seconds / 1 minute?
'''

def round_to_n(x, n):
    """ Rounds x to n significant digits"""
    if x != 0:
        return float(round(x, -int(floor(log10(abs(x)))) + (n - 1)))
    elif x == 0:
        return 0


class ASF1430(Sensor):
    def __init__(self, uid, sensor_config, connection):
        super(ASF1430Module, self).__init__(self, uid, sensor_config)

    def byte_parser(self, bytes_in, scale_factor=70.0, zero_offset=17, num_digits=3):
        """ This parses an incoming byte string for the mass flow data """
        # Identify relevant bytes and convert hex to 16-bit signed int
        MF_msb, MF_lsb = str(bytes_in[2]), str(
            bytes_in[3])  # the 3rd and 4th bytes give unscaled mass flow data
        MF_u = int('0x' + MF_msb + MF_lsb, 16)
        if MF_u > 0x7FFF:
            MF_u -= 0x10000

        logging.debug("raw value: %d" % MF_u)  # print raw value for debugging zero offset
        MF_u += zero_offset # add zero offset. Needs some playing around with
        # Scale data to correct value (scale factor of 70 used) and round to minimize data transfer
        MF = round_to_n(MF_u / scale_factor, num_digits)
        logging.debug('corrected ml/min value: %.4f' % MF) # print final result
        
        return MF

    def get_value(self):
        hex_string = [] # array for storing received bytes
        in_bin = self.connection.read(4) # reads in four bytes of data
        
        # iterate through loop to convert into hexadecimal for manipulation
        for byte in in_bin:
            try:
                hex = binascii.hexlify(byte).decode('utf-8') # decode into hexadecimal
            except:
                logging.exception("hex conversion error")
                
            hex_string.append(hex) # append each byte to the array
        
        # check if we have 4 bytes and first two are sync bytes
        if (len(hex_string) == 4 and hex_string[0] == u'7f' and 
                hex_string[1] == u'7f'):
            return self.byte_parser(hex_string) # run byte_parser to decode data
        else: # if we don't have any data in hex_string and first two bytes aren't 7F then we are out of sync. Happens when sensor loses power.
            logging.debug('sensor disconnected or out of sync - attempting to re-sync')
            self.connection.write('s\r'.encode()) # send stop command to sensor
            self.connection.read(12) # read the response - always 12 bytes long
            self.connection.write('go\r'.encode())# send the start command to sensor
            self.connection.read(4) # read the response - always 4 bytes long. After this, reading next 4 bytes, we should be in sync again


class ASF1430Module(NodeModule):
    def __init__(self, *args, **kwargs):
        super(ASF1430Module, self).__init__(*args, **kwargs)
        self.connection = serial.Serial(
            "COM6", 19200, timeout=1)

        sensor_config = {
            "name": "MassFlow",
            "units": "ml/min",
            "brick_tag": "Mass_Flow_Sensor",
            "variance": 1,
        }
        self.sensor = ASF1430('asf1430', sensor_config, self.connection)
        self.sensor.register_callback(self.push)

    def cleanup(self):
        self.connection.close()

    def tick(self):
        self.sensor.roc()
        self.wait(0.01)
