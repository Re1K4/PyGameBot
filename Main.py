######################################################
# import
######################################################
import pyautogui as pg
import time
import logging
import os
import keyboard
import threading
import win32gui
import cv2
import numpy as np
import Control
import Action
import SharedVariable as sv
from Event import Event as ev
from Timer import Timer as tm
from TemplateMatching import TemplateMatching as im

######################################################
# Global Settings
######################################################

# Logging settings
logger = logging.getLogger(">")
logging.basicConfig(level=logging.INFO,
                    format=" %(asctime)s - %(levelname)s:%(name)s - %(message)s",
                    #filename = os.path.dirname(__file__) + "/log.txt"
                    )

######################################################
# Functions
######################################################

# Function to force exit (multithreaded)
def check_esc_key():
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed('esc'):
            logger.info("ESC key pressed, End Script")
            sv.exit_loop = True
            break
t = threading.Thread(target=check_esc_key)
t.start()

# Function to initialize window coordinates (maintaining window size)
def initWindow(app_name):
    logger.info("Init Window Position")
    app_window = win32gui.FindWindow(None, app_name)
    time.sleep(2)
    win32gui.SetForegroundWindow(app_window)
    x0, y0, x1, y1 = win32gui.GetWindowRect(app_window)
    sv.window_size_x = x1 - x0
    sv.window_size_y = y1 - y0
    sv.window_center_x = sv.window_size_x // 2
    sv.window_center_y = sv.window_size_y // 2
    win32gui.MoveWindow(app_window, 0, 0, sv.window_size_x, sv.window_size_y, True)

######################################################
# Event Object 
# Class for comparison with coordinates and color values
# INIT : ev([int] x, [int] y, [tuple]([int] R,[int] G,[int] B)) return object
    #x : x-coordinate
    #y : y-coordinate
    #RGB : Colorvalue
# METHOD : checkColor(self) return bool
    #Compares pixel colors at specified coordinates
######################################################
FindEnemy = ev(554,71,(254,0,0))
MyHP = ev(0,0,(255,255,255))

######################################################
# Timer Object
# Class for measure time
# INIT : tm() return object
# METHOD : set(self) return None
    #Record the time at the time of the call and activate the in-use flag
# METHOD : distance(self) return float
    #Calculate the time difference from the last time set() was called
# METHOD : reset(self) return None
    #Reset the timer so that it can be set again.
######################################################
FindEnemy_tm = tm()

######################################################
# TemplateMatching Object
# Class for template matching
# INIT : im([any] image_filename) return object
    #image_filename : File path of template image
# METHOD : match(self,[tuple]([int] x,[int] y,[int] w,[int] h),[float]fuzzy) return BOX or None
    #xywh : Top-left coordinate, width and height of the rectangular area for template matching
    #fuzzy : Matching accuracy value (low-high/0-1)
# METHOD : match_binary(self,[tuple]([int] x,[int] y,[int] w,[int] h),[float]fuzzy) return BOX or None
    #Same as match(), but binarizes the template image before matching
# CLASSMETHOD : cv_display() return None
    #If cv_display_flag is True, draw matching results in real time
######################################################
Enemy = im('test.png')

######################################################
# Main
######################################################
logger.info(os.path.basename(__file__) + " START")

# App name
app_name = "Game Window Name"
initWindow(app_name)

# Display TemplateMatching result on/off
im.cv_display_flag = False

# Main process
while not sv.exit_loop:
    # Initial state
    if Control.NOW == 0:
        Control.changeCtrl(1)
        logger.info("Find Enemy")

    # Enemy search
    if Control.NOW == 1:
        FindEnemy_tm.set()
        # Enemy found
        if FindEnemy.checkColor() == True:
            Control.changeCtrl(2)
            logger.info("Attack")
            FindEnemy_tm.reset()
        # Search time exceeded
        elif FindEnemy_tm.distance() > 7:
            Control.changeCtrl(10)
            logger.info("Not Find")
            FindEnemy_tm.reset()
        # Search for enemy
        else:
            Action.camera_reset()
            Action.enemy_lockon()
        """
        #Example code for finding the enemy using template matching
        if Enemy.match((0,0,sv.window_size_x,sv.window_size_y),0.8) != None:
            Control.changeCtrl(2)
            logger.info("Attack")
            FindEnemy_tm.reset()
        """

    # Attack
    if Control.NOW == 2:
        if FindEnemy.checkColor() == False:
            Control.changeCtrl(0)
            logger.info("Enemy Died")
        else:
            Action.attack()
            if MyHP.checkColor() == False:
                Action.use_portion()

    # Enemy search (time exceeded)
    if Control.NOW == 10:
        Action.Turn_camera_right()
        Action.enemy_lockon()
        if FindEnemy.checkColor() == True:
            Control.changeCtrl(2)
            logger.info("Attack")

cv2.destroyAllWindows()