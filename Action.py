#Simple action processing
import pyautogui as pg
import time

def enemy_lockon():
    pg.click(button='middle')
    time.sleep(0.25)

def Turn_camera_right():
    pg.keyDown('right')
    time.sleep(0.45)
    pg.keyUp('right')

def attack():
    pg.mouseDown()
    time.sleep(0.1)
    pg.mouseUp()

def use_portion():
    pg.keyDown('3')
    time.sleep(0.1)
    pg.keyUp('3')

def camera_reset():
    pg.keyDown('l')
    time.sleep(0.1)
    pg.keyUp('l')
