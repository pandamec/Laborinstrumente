import serial
import time


class device:
    def __init__(self,
                 COM):
        self.COM=COM
        self.ser = serial.Serial(COM, 115200, timeout=1)
        self.ser.setDTR(False)
        self.ser.setRTS(False)

    def setChannels(self,ch1,ch2):

        time.sleep(2)
        self.ser.reset_input_buffer()

        #ch1 = 0 2 4 6
        #ch2 = 1 3 5 7

        cmd = f"CH{ch1} CH{ch2}\n"
        self.ser.write(cmd.encode())

        time.sleep(1)

        for _ in range(5):
            line = self.ser.readline().decode(errors='ignore').strip()
            if line:
                print(line)



