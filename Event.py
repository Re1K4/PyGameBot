import pyautogui as pg
import logging

logger = logging.getLogger(">")

class Event:
    def __init__(self,check_x,check_y,check_color):
        self.x = check_x
        self.y = check_y
        self.c = check_color

    def checkColor(self):
        logger.debug((f"screen : {pg.pixel(self.x,self.y)} = {self.c}"))
        return pg.pixelMatchesColor(self.x, self.y, self.c)
        #return pg.pixelMatchesColor(self.x, self.y, self.c,tolerance=5)