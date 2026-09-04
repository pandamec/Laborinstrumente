## Preamble
import sys
sys.path.append(r"C:\TUC\03 Scripts\Laborinstrumente\src") #Folder of the library
import Monitor224

## Configuration
monitor=Monitor224.device("a") #Only the channel connected to the instrument

## Command
monitor.getTemperature() #Read the temperature