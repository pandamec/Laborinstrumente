
import time
from .PrologixGPIB import PrologixGPIB

class Device(PrologixGPIB):
    """Keithley 2182A NanovoltMeter"""


    def reset(self):
        self.send_instr('*RST')
        time.sleep(0.5)

    def idn(self):
        return self.query('*IDN?')

    def RS232_mode(self):
        self.send_instr('SYST:COMM:STAT ON')
        self.send_instr('SYST:COMM:SER:TERM CR')
        self.send_instr('SYST:COMM:SER:BAUD 19.2k')
        self.send_instr('SYST:COMM:SER:FLOW XON')