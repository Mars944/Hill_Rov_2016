#include <Wire.h>
#include "MS5837.h"

MS5837 pressureSensor;

void setup() {
  
  Serial.begin(9600);  
  Wire.begin();

  pressureSensor.init();
  pressureSensor.setFluidDensity(997); // kg/m^3 (997 freshwater, 1029 for seawater)
}

void loop() {

  sensor.read();

  Serial.print("Depth: "); 
  Serial.print(sensor.depth()); 
  Serial.println(" m");
  
  delay(1000);
}
