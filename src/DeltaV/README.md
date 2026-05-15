The code setups Keithley 2182A and Keithley 6221 for remote measurements. This can also be done manually like described below.
Reference Link: https://www.tek.com/en/support/faqs/how-to-configure-the-model-6220-6221-and-2182a-for-delta-mode

Manual Setup:

2218A
1. RESTR                    restore factory default for know settings
2. SHIFT+RS-232 --> ON      activate device communication, set settings (default - Baud:19.2k , Flow control: XonXoff, Terminator: CR)

6221
1. SETUP --> PRESET --> ENTER    restore factory default for know settings
2. COMM --> GBIP --> ENTER       activate device communication, ensure settings match 2218A (do if default is unchanged)
3. SETUP --> PULSE --> ENTER     set measurement settings (refer to user manual for more information)
   3.1  I-High       - pulse peak value
   3.2  I-Low        - value for pulse off
   3.3. Width        - pulse width 
   3.4. Count        - amount of measurements
   3.5. SDEL         - delay between peak start and measurement start (recommended to be width/2)
   3.6. Range        - source range adjusted automatically (BEST) or fixed (FIXED)
   3.7. Interval     - off time after the pulse (PLC = power supply wavenumbers (3 for measurements, rest = off time)
   3.8. Low Measure  - change to 2-point measurement
4. UNITS --> OHMS --> ENTER       measure in Ohms
5. PULSE                          arm pulse mode (2218A should show "PULSE MODE")
6. EXIT                           end measurement
7. Recall
   7.1.  up/down  - show single measurements in buffer
   7.2.  edit     - show statistics (Min, Max, Avg, StdDev, peak-to-peak
