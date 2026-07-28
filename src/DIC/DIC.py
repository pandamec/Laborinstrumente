import ctypes
import time
import sys

sys.path.append(r"C:\TUC\03 Scripts\Laborinstrumente\src\DIC")
import tisgrabber as tis

class Device:
    
   def __init__(self,
                 parameters,
                 wait_frame_ms=2000):

        self.wait_frame_ms=wait_frame_ms
        self.ic = ctypes.cdll.LoadLibrary(r"C:\TUC\03 Scripts\Laborinstrumente\src\DIC\tisgrabber_x64.dll")
        tis.declareFunctions(self.ic)
        self.ic.IC_InitLibrary(0)
        self.kamera = self.ic.IC_LoadDeviceStateFromFile(None,tis.T(parameters))

   def startLive(self):
       self.ic.IC_StartLive(self.kamera,1)

   def snapImage(self):
       self.ic.IC_SnapImage(self.kamera, self.wait_frame_ms)
       print("snap")

   def saveImage(self,filepath):

         #f"test_DIC\\260713_test{counter:04d}.bmp")
         
       self.ic.IC_SaveImage(self.kamera, tis.T(filepath), tis.ImageFileTypes['BMP'], 90)


