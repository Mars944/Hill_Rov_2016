# TSYS01 module
# Requires Wire to be imported through nanpy
"""May Require that ctypes be imported into Main.py"""

from nanpy import wire
from ctypes import (c_uint8, c_uint16, c_uint32)

# I2C Addresses (Hex Values)
TSYS01_ADDR=0x77  
TSYS01_RESET=0x1E
TSYS01_ADC_READ=0x00
TSYS01_ADC_TEMP_CONV=0x48
TSYS01_PROM_READ=0XA0

class TSYS01(): #Takes arduino object
        
        def __init__(self, arduino):
                # Private Variables
                self._C = [None]*8 # Will receive uint16_t
                self._D1 = None    # Will receive uint32_t 
                self._TEMP = None  # Will receive float
                self._adc = None   # Will receive uint32_t

                self.arduino = arduino

                # Reset the TSYS01, per datasheet
                wire.beginTransmission(TSYS01_ADDR)
                wire.write(TSYS01_RESET)
                wire.endTransmission()

                arduino.delay(10)
        
                # Read calibration values
                for i in range(8):
                        wire.beginTransmission(TSYS01_ADDR)
                        wire.write(TSYS01_PROM_READ+c_uint8(i)*2)
                        wire.endTransmission()

                        wire.requestFrom(TSYS01_ADDR,2)
                        self._C[c_uint8(i)] = (wire.read() << 8) | wire.read()
        

        def read(self):
                wire.beginTransmission(TSYS01_ADDR)
                wire.write(TSYS01_ADC_TEMP_CONV)
                wire.endTransmission()
         
                arduino.delay(10) # Max conversion time per datasheet
                
                wire.beginTransmission(TSYS01_ADDR)
                wire.write(TSYS01_ADC_READ)
                wire.endTransmission()

                wire.requestFrom(TSYS01_ADDR,3)
                self._D1 = c_uint32(0)
                self._D1 = wire.read()
                self._D1 = (self._D1 << 8) | wire.read()
                self._D1 = (self._D1 << 8) | wire.read()

                calculate()

        def readTestCase(self):
                self._C[0] = c_uint16(0)
                self._C[1] = c_uint16(28446)  #0xA2 K4
                self._C[2] = c_uint16(24926)  #0XA4 K3
                self._C[3] = c_uint16(36016)  #0XA6 K2
                self._C[4] = c_uint16(32791)  #0XA8 K1
                self._C[5] = c_uint16(40781)  #0XAA K0
                self._C[6] = c_uint16(0)
                self._C[7] = c_uint16(0)

                self._D1 = c_uint32(9378708.0) #...0f
        
                self._adc = c_uint32(self._D1/256)

                calculate()

        def temperature(self):
                return self._TEMP

        def __calculate__(self):
                self._adc = c_uint32(self._D1/256)

                TEMP = (-2) * float(self._C[1]) / 1000000000000000000000.0 * pow(self._adc,4) + 4 * float(self._C[2]) / 10000000000000000.0 * pow(self._adc,3) +(-2) * float(self._C[3]) / 100000000000.0 * pow(self._adc,2) +1 * float(self._C[4]) / 1000000.0 * self._adc +(-1.5) * float(self._C[5]) / 100
#               TEMP = (-2) * float(self._C[1]) / 1000000000000000000000.0f * pow(self._adc,4) + 4 * float(self._C[2]) / 10000000000000000.0f * pow(self._adc,3) +(-2) * float(self._C[3]) / 100000000000.0f * pow(self._adc,2) +1 * float(self._C[4]) / 1000000.0f * self._adc +(-1.5) * float(self._C[5]) / 100
