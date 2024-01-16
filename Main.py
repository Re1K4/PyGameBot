######################################################
#Game Automation with Python PyAutoGui library
#Developer:reika00
######################################################

######################################################
# include
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

#ログ出力設定
logger = logging.getLogger(">")
logging.basicConfig(level=logging.INFO,
                    format=" %(asctime)s - %(levelname)s:%(name)s - %(message)s",
                    #filename = os.path.dirname(__file__) + "/log.txt"
                    )

######################################################
# Functions
######################################################

#強制終了関数(マルチスレッド)
def check_esc_key():
    while True:
        time.sleep(0.01)
        if keyboard.is_pressed('esc'):
            logger.info("ESC key pressed, End Script")
            sv.exit_loop = True
            break
t = threading.Thread(target=check_esc_key)
t.start()

# ウィンドウ座標初期化関数(ウィンドウサイズは維持)
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
######################################################
FindEnemy = ev(554,71,(254,0,0))
FindEnemy_2 = ev(554,76,(254,0,0))
FindEnemy_3 = ev(554,80,(254,0,0))
HP = ev(780,590,(42,255,168))

######################################################
# Timer Object
######################################################
FindEnemy_tm = tm()

######################################################
# TemplateMatching Object
######################################################
EnemyNameStr = im('lv.png')

######################################################
# Main
######################################################
logger.info(os.path.basename(__file__) + " START")

#アプリ名
app_name = "BLUE PROTOCOL  "
initWindow(app_name)

# 認識画面描画on/off
im.cv_display_flag = False

# メイン処理
while not sv.exit_loop:
    #初期状態
    if Control.NOW == 0:
        Control.changeCtrl(1)
        logger.info("Find Enemy")

    #エネミーサーチ
    if Control.NOW == 1:
        FindEnemy_tm.set()
        #敵を発見
        if FindEnemy.checkColor() == True or FindEnemy_2.checkColor() == True or FindEnemy_3.checkColor() == True:
            Control.changeCtrl(2)
            logger.info("Attack")
            FindEnemy_tm.reset()
        #探索時間を超過
        elif FindEnemy_tm.distance() > 7:
            Control.changeCtrl(10)
            logger.info("Not Find")
            FindEnemy_tm.reset()
        #敵を探索
        else:
            Action.camera_reset()
            Action.enemy_lockon()

    #攻撃
    if Control.NOW == 2:
        if FindEnemy.checkColor() == False and FindEnemy_2.checkColor() == False and FindEnemy_3.checkColor() == False:
            Control.changeCtrl(0)
            logger.info("Enemy Died")
            #倒し漏らし対策
            Action.attack_archer()
        else:
            Action.attack_archer()
            if HP.checkColor() == False:
                Action.use_portion()

    #エネミーサーチ(時間超過)
    if Control.NOW == 10:
        Action.Turn_camera_right()
        Action.enemy_lockon()
        if FindEnemy.checkColor() == True or FindEnemy_2.checkColor() == True or FindEnemy_3.checkColor() == True:
            Control.changeCtrl(2)
            logger.info("Attack")

        """
        if EnemyNameStr.match((0,0,sv.window_size_x,sv.window_size_y),0.8) != None:
            EnemyNameStr.moveCenter((0,0,sv.window_size_x,sv.window_size_y),0.8)
            Control.changeCtrl(1)
            logger.info("Find Enemy")
        """

cv2.destroyAllWindows()