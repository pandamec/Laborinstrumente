## Preamble
import sys
sys.path.append(r"C:\TUC\03 Scripts\Laborinstrumente\src") #Folder of the library
import Controller336

## Configuration
controller=Controller336.device("a") #Only the channel connected to the instrument

## Command
controller.getTemperature() #Read the temperature