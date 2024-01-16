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

# 画像ファイルのpathに日本語指定を可能にする関数
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

class TemplateMatching:
    #クラス変数
    cv_display_flag = False
    result = None

    #クラスメソッド
    #マッチング結果の画面描画
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

    #コンストラクタ
    def __init__(self,filename):
        self.image = imread(os.path.dirname(os.path.abspath(__file__)) + "\\" + filename)

    #テンプレートマッチング
    def match(self,xywh,fuzzy):
        TemplateMatching.result = pg.locateOnScreen(self.image,grayscale=True,region=xywh,confidence=fuzzy)
        logger.debug(f"TemplateMatching.result = {TemplateMatching.result}")
        return TemplateMatching.result
    
    #二値化テンプレートマッチング
    def match_binary(self,xywh,fuzzy):
        #テンプレート画像をグレースケール⇒二値化
        glay_temp = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        _, binary_temp = cv2.threshold(glay_temp, 127, 255, cv2.THRESH_BINARY)
        #スクリーンショットを取得しグレースケール⇒二値化
        screenshot = pg.screenshot(region=xywh)
        glay_screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        _, binary_screen = cv2.threshold(glay_screen, 127, 255, cv2.THRESH_BINARY)
        #テンプレートマッチング
        matching_map = cv2.matchTemplate(binary_screen, binary_temp, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(matching_map)
        #曖昧度以上の一致を確認
        if max_val < fuzzy:
            TemplateMatching.result = None
        else:
            #左上座標と幅、高さのタプルを返す
            TemplateMatching.result = (max_loc[0],max_loc[1],self.image.shape[1],self.image.shape[0])
        logger.debug(f"TemplateMatching.result = {TemplateMatching.result}")
        return TemplateMatching.result
    
    """
    def moveCenter(self,xywh,fuzzy):
        while self.match(xywh,fuzzy) != None:
            time.sleep(0.1)
            x, y, w, h = TemplateMatching.result
            center_x_delta = sv.window_center_x - x
            center_y_delta = sv.window_center_y - y
            if (abs(center_x_delta) > sv.window_size_x // 8):
                logger.debug(f"x:{center_x_delta} fix")
                if center_x_delta > 0:
                    pg.keyDown('left')
                    time.sleep(0.01)
                    pg.keyUp('left')
                elif center_x_delta < 0:
                    pg.keyDown('right')
                    time.sleep(0.01)
                    pg.keyUp('right')
            if (abs(center_y_delta) > sv.window_size_y // 8):
                logger.debug(f"y:{center_y_delta} fix")
                if center_y_delta > 0:
                    pg.keyDown('up')
                    time.sleep(0.01)
                    pg.keyUp('up')
                elif center_y_delta < 0:
                    pg.keyDown('down')
                    time.sleep(0.01)
                    pg.keyUp('down')
            if (abs(center_x_delta) < sv.window_size_x // 8) and (abs(center_y_delta) < sv.window_size_y // 8):
                logger.debug("moveCenter break")
                break
    """
    
i = threading.Thread(target=TemplateMatching.cv_display)
i.start()