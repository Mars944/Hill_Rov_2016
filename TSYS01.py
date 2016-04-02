# TSYS01 module
# Requires Wire to be imported through nanpy
"""May Require that ctypes be imported into Main.py"""

from nanpy import wire

# I2C Addresses (Hex Values)
TSYS01_ADDR=0x77  
TSYS01_RESET=0x1E
TSYS01_ADC_READ=0x00
TSYS01_ADC_TEMP_CONV=0x48
TSYS01_PROM_READ=0xA0

class TSYS01(): # Temperature Sensor object
        
        def __init__(self, arduino):
                # Private Variables
                self._C = [0]*8 # Needs to receive uint16_t
                self._D1 = 0    # Needs to receive uint32_t
                self._TEMP = 0.0  # Needs to receive float
                self._adc = 0   # Needs to receive uint32_t

                self.arduino = arduino

                # Reset the TSYS01, per datasheet
                masterWire = wire.Wire()

                wire.begin()
                wire.beginTransmission(TSYS01_ADDR)
                wire.write(TSYS01_RESET)
                wire.endTransmission()

                sleep(.01) # arduino.delay(10) if fails
        
                # Read calibration values
                for i in range(8):
                        wire.beginTransmission(TSYS01_ADDR)
                        wire.write(TSYS01_PROM_READ+i*2)
                        wire.endTransmission()

                        wire.requestFrom(TSYS01_ADDR,2)
                        self._C[i] = (wire.read() << 8) | wire.read()
        

        def read(self):
                wire.beginTransmission(TSYS01_ADDR)
                wire.write(TSYS01_ADC_TEMP_CONV)
                wire.endTransmission()
         
                sleep(.01) # arduino.delay(10) if fails
                
                wire.beginTransmission(TSYS01_ADDR)
                wire.write(TSYS01_ADC_READ)
                wire.endTransmission()

                wire.requestFrom(TSYS01_ADDR,3)
                self._D1 = 0
                self._D1 = wire.read()
                self._D1 = (self._D1 << 8) | wire.read()
                self._D1 = (self._D1 << 8) | wire.read()

                calculate()

        def readTestCase(self):
                self._C[0] = 0
                self._C[1] = 28446  #0xA2 K4
                self._C[2] = 24926  #0XA4 K3
                self._C[3] = 36016  #0XA6 K2
                self._C[4] = 32791  #0XA8 K1
                self._C[5] = 40781  #0XAA K0
                self._C[6] = 0
                self._C[7] = 0

                self._D1 = 9378708.0 #...0f
        
                self._adc = self._D1/256

                calculate()

        def temperature(self):
                return self._TEMP

        def __calculate__(self):
                self._adc = c_uint32(self._D1/256)

                TEMP =  (-2) * float(self._C[1]) / 1000000000000000000000.0 * self.adc**4 + 4 * float(self._C[2]) / 10000000000000000.0 * self._adc**3 +(-2) * float(self._C[3]) / 100000000000.0 * self._adc**2 +1 * float(self._C[4]) / 1000000.0 * self._adc +(-1.5) * float(self._C[5]) / 100.0
