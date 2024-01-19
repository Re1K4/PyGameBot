import logging
import cv2
import os
import pyautogui as pg
import numpy as np
import SharedVariable as sv
import time
import threading
import win32gui

logger = logging.getLogger(">")

# Allow non-ASCII characters to be included in the path of image files
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

class TemplateMatching:
    #CLASS VARIABLE
    cv_display_flag = False
    result = None

    #CLASS METHOD
    @classmethod
    def cv_display(self):
        while sv.exit_loop == False:
            time.sleep(0.1)
            if  TemplateMatching.cv_display_flag == True:
                screenshot = pg.screenshot(region=(0,0,sv.window_size_x,sv.window_size_y))
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
                if TemplateMatching.result != None:
                    x, y, w, h = TemplateMatching.result
                    cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imshow('cv_display', screenshot)
                cv2.waitKey(1)

    def __init__(self,filename):
        self.image = imread(os.path.dirname(os.path.abspath(__file__)) + "\\" + filename)

    def match(self,xywh,fuzzy):
        TemplateMatching.result = pg.locateOnScreen(self.image,grayscale=True,region=xywh,confidence=fuzzy)
        logger.debug(f"TemplateMatching.result = {TemplateMatching.result}")
        return TemplateMatching.result
    
    def match_binary(self,xywh,fuzzy):
        #Template image grayscale => binarize
        glay_temp = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary_temp = cv2.threshold(glay_temp, 127, 255, cv2.THRESH_BINARY)
        #Get screenshot grayscale => binarize
        screenshot = pg.screenshot(region=xywh)
        glay_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        _, binary_screen = cv2.threshold(glay_screen, 127, 255, cv2.THRESH_BINARY)
        #Template matching
        matching_map = cv2.matchTemplate(binary_screen, binary_temp, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(matching_map)
        #Compare accuracy values with the highest similarity part in the matching map
        if max_val < fuzzy:
            TemplateMatching.result = None
        else:
            #Returns a tuple of the upper-left coordinates, width, and height of the matched rectangle
            TemplateMatching.result = (max_loc[0],max_loc[1],self.image.shape[1],self.image.shape[0])
        logger.debug(f"TemplateMatching.result = {TemplateMatching.result}")
        return TemplateMatching.result
    
i = threading.Thread(target=TemplateMatching.cv_display)
i.start()