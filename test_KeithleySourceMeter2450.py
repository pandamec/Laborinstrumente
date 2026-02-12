# Version 1.0 18SEP2025

## Preamble
import sys
sys.path.append(r"E:\Programs\Laborinstrumente\src") # Path where folder Keithley2400 is
import Keithley2450

## Configuration
COM_PORT = 'COM7'   # Find the port in the list of device manager
GPIB_ADDR = 1       # From the menu->communication in the front panel of the instrument

keithley = Keithley2450.Device(COM_PORT, GPIB_ADDR) # Set the word keithley to call the functions from the instrument
print("Connected to:", keithley.idn()) # check if the device is connected. It should be "KEITHLEY INSTRUMENTS INC.,MODEL 2400,1330776,C32   Oct  4 2010 14:20:11/A02  /R/J" or similar

## Measurement commands

"""The four wire measurement is carried out with the following commands in this order"""
#keithley.enable_4wire()
#keithley.source_CurrentMode()
#keithley.set_CurrentRange(1E-3) # 1E-3 = 1 mA
#keithley.set_current(0.25e-3)    # 0.1e-3 = 0.1m A
#keithley.set_VoltageCompliance(5) # 1V
#keithley.set_VoltageSense()
#keithley.set_VoltageRange(1) # 1V
#keithley.output_on()  # The instrument will only start when the above parameters are defined.
#keithley.output_off() # Stop the current generation