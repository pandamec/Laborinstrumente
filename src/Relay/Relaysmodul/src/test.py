
import serial
import time

# Replace 'COM3' with your ESP32 port
COM='COM7'
ser = serial.Serial(COM, 115200, timeout=1)
time.sleep(5)

ch1 = "0b0001000000001000\n"

ser.write(ch1.encode())

#time.sleep(1)

print(ser.readline().decode().strip())

