import time
from .PrologixGPIB import PrologixGPIB


class Device(PrologixGPIB):
    """Keithley 6221 CurrentSource"""

    #start setup
    def reset(self):
        self.send_instr('*RST')
        time.sleep(0.5)


    def idn(self):
        return self.query('*IDN?')

        ## Setup Pulse Delta Mode

        # missing: GBIP connnection


    def setup_device_communication(self):
        """settings for communication between 6221 and 2182A"""
        self.send_instr('SYST:COMM:SER:TERM CR')
        self.send_instr('SYST:COMM:SER:BAUD 19.2k')
        self.send_instr('SYST:COMM:SER:FLOW XON')



    #device setup
    def set_unit(self):
        """set measurements to Ohms"""
        #self.send_instr('UNIT[:VOLT][:DC] OHMS')
        self.send_instr('UNIT OHMS')


    def set_pulse_high(self, value):
        """set puls peak"""
        #self.send_instr('SOUR:PDEL:HIGH 1e-3')
        self.send_instr(f'SOUR:PDEL:HIGH {value}')


    def set_pulse_low(self):
        """set puls offstate"""
        self.send_instr('SOUR:PDEL:LOW 0')


    def set_pulse_width(self, value):
        """set puls width"""
         #self.send_instr('SOUR:PDEL:WIDT 110e-6')
        self.send_instr(f'SOUR:PDEL:WIDT {value}')


    def set_pulse_delay(self, value):
        """set delay after pulse before it's measured """
        # self.send_instr('SOUR:PDEL:SDEL 55e-6')
        self.send_instr(f'SOUR:PDEL:SDEL {value}')


    def set_pulse_range(self):
        """set puls range"""
        self.send_instr('SOUR:PDEL:RANG BEST')


    def set_pulse_count(self, value):
        """set puls count"""
        # self.send_instr('SOUR:PDEL:COUN 100')
        self.send_instr(f'SOUR:PDEL:COUN {value}')


    def set_pulse_interval(self, value):
        """set puls interval, wait time before next pulse"""
        # self.send_instr('SOUR:PDEL:INT 10')
        self.send_instr(f'SOUR:PDEL:INT {value}')

    def set_buffer(self, value):
        """read the values saved in buffer"""
        # self.send_instr('TRAC:POIN 100')
        self.send_instr(f'TRAC:POIN {value}')
        #check if necessary

    def set_ASCII_string(self,):
        """read the values saved in buffer"""
        self.send_instr('FORM:ELEM READ, TST, UNIT, SOUR') #check necessary outputs

    def set_NPLC(self):
        """set 2182A integration time"""
        self.send_instr('SYST:COMM:SER:SEND "SENS:VOLT:DC:NPLC 1"') # Integration time already included
        self.send_instr('SYST:COMM:SER:SEND "SENS:VOLT:DC:NPLC?"')
        return self.query('SYST:COMM:SER:ENT?')



    def set_pulse_mode(self):
        """set measurement mode to deltamode"""
        self.send_instr('SOUR:PDEL:LME 2')


    def set_pulse_mode(self):
        """arm puls mode"""
        self.send_instr('SOUR:PDEL:ARM')



    #tool control
    def check_pulse_mode(self):
        """check if pulse mode is armed"""
        return self.query('SOUR:PDEL:ARM?')


    def disarm_pulse_mode(self):
        """disarm pulse mode"""
        self.send_instr('SOUR:SWE:ABOR')


    def output_on(self):
        """Turn the instrument on"""
        self.send_instr(':OUTP ON')


    def output_off(self):
        """Turn the instrument off"""
        self.send_instr(':OUTP OFF')


    def start_measurement(self):
        """start measurement"""
        self.send_instr('INIT:IMM')



    #read measurements
    def read_pre_math(self):
        """read the last values sensed (pre Deltamath value)"""
        return self.query('SENS:DATA?')

    def read_buffer(self):
        """read the values saved in buffer"""
        return self.query('TRAC:DATA?')


#checks
    def check_query(self):
        """check if finished"""
        return self.query('*OPC?')

    
    def check_error(self):
        """check if error"""
        return self.query('SYST:ERR?')