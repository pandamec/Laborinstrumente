import pyautogui
import pygetwindow as gw
import time
import sys

class Device:
    
    def __init__(self,window_title):

        self.window_title=window_title
        self.CONFIDENCE = 0.85
        self.MOVE_DURATION = 0.3
        self.CLICK_DELAY = 5

        pyautogui.FAILSAFE = True


        self.path_measurement=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\measurement.png"
        self.path_save=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\save.png"
        self.path_saveBottom=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\saveBottom.png"
        self.path_export=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\export.png"
        self.path_msadd=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\msadd.png"
        self.path_mnew=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\mnew.png"
        self.path_closeothers=r"C:\TUC\03 Scripts\Laborinstrumente\src\TOCS\icons\closeothers.png"


    def activate_window(self):
        """
        Find and activate target window.
        """

        windows = gw.getWindowsWithTitle(self.window_title)

        if not windows:
            raise Exception(f"Window not found: {self.window_title}")

        win = windows[0]

        if win.isMinimized:
            win.restore()

        win.activate()

        time.sleep(1)

        print(f"Activated window: {win.title}")

        return win


    def find_and_click(self,image_path,
                    timeout=15):
        """
        Search for image on screen and click it.
        """

        print(f"Searching for: {image_path}")

        start_time = time.time()

        while True:

            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=self.CONFIDENCE
            )

            if location is not None:

                x, y = location

                print(f"Found {image_path} at ({x}, {y})")

                pyautogui.moveTo(
                    x,
                    y,
                    duration=self.MOVE_DURATION
                )

                pyautogui.click()

                time.sleep(self.CLICK_DELAY)

                return True

            if time.time() - start_time > timeout:
                raise Exception(f"Timeout finding image: {image_path}")

            time.sleep(0.5)


    def find_and_rightclick(self,image_path,
                    timeout=15):
        """
        Search for image on screen and click it.
        """

        print(f"Searching for: {image_path}")

        start_time = time.time()

        while True:

            location = pyautogui.locateCenterOnScreen(
                image_path,
                confidence=self.CONFIDENCE
            )

            if location is not None:

                x, y = location

                print(f"Found {image_path} at ({x}, {y})")

                pyautogui.moveTo(
                    x,
                    y,
                    duration=self.MOVE_DURATION
                )

                pyautogui.click(button='right')

                time.sleep(self.CLICK_DELAY)

                return True

            if time.time() - start_time > timeout:
                raise Exception(f"Timeout finding image: {image_path}")

            time.sleep(0.5)

    def run_measurement(self):
        
        try:

            # Activate remote software window
            self.activate_window()

            time.sleep(2)

            self.find_and_click(self.path_measurement)

            time.sleep(180)

            self.find_and_click(self.path_save)
            time.sleep(2)
            
            self.find_and_click(self.path_saveBottom)
            time.sleep(2)
            
            self.find_and_click(self.path_export)
            time.sleep(2)

            self.find_and_click(self.path_saveBottom)
            time.sleep(2)

            self.find_and_click(self.path_msadd)
            time.sleep(2)

            self.find_and_rightclick(self.path_mnew)
            time.sleep(2)

            self.find_and_click(self.path_closeothers)
            time.sleep(2)
    

        except Exception as e:

            print(f"\nERROR: {e}")
            sys.exit(1)