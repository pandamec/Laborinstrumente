sys.path.append(r"E:\00 Script\AttodryMeasurement\src") #Folder of the library
import MUX


COM = 'COM10'

ch1 = 0 #0 2 4 6
ch2 = 1 # 1 3 5 7

mux=MUX.device(COM)

mux.setChannels(ch1,ch2)