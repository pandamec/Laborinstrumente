
import time

from .PrologixGPIB import PrologixGPIB

class Device(PrologixGPIB):
    """Keithley 2400 SourceMeter"""
    def reset(self):
        self.send_instr('*RST')
        time.sleep(0.5)

    def idn(self):
        return self.query('*IDN?')

    ## Voltage Mode (not tested)
    #def enable_4wire(self):
     #   self.send_instr(':SYST:RSEN ON')

    #def disable_4wire(self):
     #   self.send_instr(':SYST:RSEN OFF')

    ## Voltage Mode
    #def source_VoltageMode(self):
     #   self.send_instr(':SOUR:FUNC VOLT')
      #  self.send_instr(':SOUR:VOLT:MODE FIXED')

    #def set_voltage(self, value):
     #   self.send_instr(f':SOUR:VOLT {value}')

    #def get_current(self):
     #   self.send_instr(':FORM:ELEM CURR')
      #  return self.query(':READ?')

    #def set_current_compliance(self, value):
     #   self.send_instr(f':SENS:CURR:PROT {value}')

    ## Current Mode

    def enable_4wire(self):
        """Enable the 4 wire measurement"""
        self.send_instr(':SYST:RSEN ON')

    def source_CurrentMode(self):
        """Set the instrument to generate current"""
        self.send_instr(':SOUR:FUNC CURR')
        self.send_instr(':SOUR:CURR:MODE FIX')

    def set_CurrentRange(self, value):
        """Set the current range in ampers"""
        self.send_instr(f':SOUR:CURR:RANG {value}')

    def set_current(self, value):
        """Set the current value in ampers"""
        self.send_instr(f':SOUR:CURR:LEV {value}')

    def set_VoltageCompliance(self, value):
        """Maximum voltage limit that the instrument will allow"""
        self.send_instr(f':SENS:VOLT:PROT {value}')


    def set_VoltageSense(self):
        """Set the instrument to measure voltage"""
        self.send_instr(':SENS:FUNC "VOLT"')

    def set_VoltageRange(self, value):
        """Set the voltage range and the format for reading :Voltage,Current"""
        self.send_instr(f':SENS:VOLT:RANG {value}')
        self.send_instr(':FORM:ELEM VOLT,CURR')

    def get_Mess(self):
        """Get an instant measurement in the format Voltage,Current"""
        return self.query(':READ?')

    def output_on(self):
        """Turn the instrument on"""
        self.send_instr(':OUTP ON')

    def output_off(self):
        """Turn the instrument off"""
        self.send_instr(':OUTP OFF')