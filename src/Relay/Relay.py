import serial
import time


class device:
    def __init__(self,
                 COM):
        self.COM=COM
        self.ser = serial.Serial(COM, 115200, timeout=1)

    def setRelays(self,array):

        self.ser.write(array.encode())
        time.sleep(1)
        self.ser.write(array.encode())
        time.sleep(1)
        self.ser.write(array.encode())
        time.sleep(1)

        print(self.ser.readline().decode().strip())
      




