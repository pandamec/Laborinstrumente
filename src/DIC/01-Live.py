'''
This sample demonstrates, how to open a camera with the
built in device selection dialog and show a live video stream.
Needed DLLs for 64 bit environment are
- tisgrabber_x64.dll
- TIS_UDSHL11_x64.dll
- tisgrabber.py
'''
import ctypes
import time

import tisgrabber as tis

ic = ctypes.cdll.LoadLibrary("./tisgrabber_x64.dll")
tis.declareFunctions(ic)

ic.IC_InitLibrary(0)

hGrabber = ic.IC_LoadDeviceStateFromFile(None,tis.T("device_for_dic_atto_2656x2296.xml"))
# hGrabber = ic.IC_LoadDeviceStateFromFile(None,tis.T("device_for_dic_2656x2296_binning2x.xml"))
if ic.IC_IsDevValid(hGrabber):
   # ic.IC_SetVideoFormat(hGrabber, tis.T("Y16 (5320x4600)"))
   #ic.IC_SetVideoFormat(hGrabber, tis.T("Y16 (2656x2296) [Binning 2x]"))
   ic.IC_StartLive(hGrabber,1)

time.sleep(1000)

#hGrabber = ic.IC_ShowDeviceSelectionDialog(None)

# # hGrabber = ic.IC_LoadDeviceStateFromFile(None,tis.T("device_for_dic_atto_2560x1920.xml"))
# hGrabber = ic.IC_LoadDeviceStateFromFile(None,tis.T("device_for_dic_atto_2560x1920_binning2x.xml"))
# if ic.IC_IsDevValid(hGrabber):
#     ic.IC_StartLive(hGrabber, 1)
#     ic.IC_MsgBox(tis.T("Click OK to stop"), tis.T("Simple Live Video"))
#     ic.IC_StopLive(hGrabber)
# else:
#     ic.IC_MsgBox(tis.T("No device opened"), tis.T("Simple Live Video"))

ic.IC_ReleaseGrabber(hGrabber)
