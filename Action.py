import pyautogui as pg
import time

def enemy_lockon():
    pg.click(button='middle')
    time.sleep(0.25)

def Turn_camera_right():
    pg.keyDown('right')
    time.sleep(0.45)
    pg.keyUp('right')
    pg.scroll(-1000)

def rolling_forward():
    pg.keyDown('w')
    time.sleep(0.1)
    pg.keyDown('ctrl')
    time.sleep(0.1)
    pg.keyUp('ctrl')
    pg.keyUp('w')

def attack_heavy_smasher():
    #基本コンボ
    pg.mouseDown(button='right')
    time.sleep(0.1)
    pg.mouseUp(button='right')
    pg.mouseDown()
    time.sleep(0.1)
    pg.mouseUp()
    #スキル
    """
    pg.keyDown('q')
    time.sleep(0.1)
    pg.keyUp('q')
    pg.keyDown('e')
    time.sleep(0.1)
    pg.keyUp('e')
    pg.keyDown('r')
    time.sleep(0.1)
    pg.keyUp('r')
    pg.keyDown('c')
    time.sleep(0.1)
    pg.keyUp('c')
    """

def battle_imagine():
    pg.keyDown('1')
    time.sleep(0.1)
    pg.keyUp('1')
    pg.keyDown('2')
    time.sleep(0.1)
    pg.keyUp('2')

def attack_archer():
    #基本コンボ
    pg.mouseDown()
    time.sleep(0.1)
    pg.mouseUp()
    pg.mouseDown()
    time.sleep(0.1)
    pg.mouseUp()
    pg.mouseDown()
    time.sleep(0.1)
    pg.mouseUp()
    pg.mouseDown()
    time.sleep(0.1)
    pg.mouseUp()
    #スキル
    """
    pg.keyDown('q')
    time.sleep(0.1)
    pg.keyUp('q')
    pg.keyDown('e')
    time.sleep(0.1)
    pg.keyUp('e')
    pg.keyDown('r')
    time.sleep(0.1)
    pg.keyUp('r')
    pg.keyDown('c')
    time.sleep(0.1)
    pg.keyUp('c')
    """

def use_portion():
    pg.keyDown('3')
    time.sleep(0.1)
    pg.keyUp('3')

def camera_reset():
    pg.keyDown('l')
    time.sleep(0.1)
    pg.keyUp('l')
