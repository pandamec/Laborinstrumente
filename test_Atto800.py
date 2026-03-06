## Preamble

import sys
sys.path.append(r"E:\CryoTOCS\CryoTOCS\src") # Replace by your path
import Atto800

## Configuration
IP = "192.168.1.1"
Atto=Atto800.Device(IP)
Atto.connect()

## Commands Sample Plate

#Atto.sample.getTemperature()
#Atto.sample.setSetPoint(100)
#Atto.sample.startTempControl()
#Atto.sample.stopTempControl()

## Commands Cold Plate

#Atto.tboard.getTemperature(0)
#Atto.exchange.setSetPoint(5)
#Atto.exchange.startTempControl()
#Atto.exchange.stopTempControl()


## Additional commands that you may need

#Atto.pressures.getSampleSpacePressure()
#Atto.sample.downloadCalibrationCurve()
#Atto.sample.getResistance()
#Atto.sample.getHeaterPower()