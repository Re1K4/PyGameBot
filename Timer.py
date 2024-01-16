import time

class Timer:
    #コンストラクタ
    def __init__(self):
        self.setTime = 0
        self.usedFlg = 0

    #タイマーセット
    def set(self):
        if self.usedFlg == 0:
            self.setTime = time.time()
            self.usedFlg = 1

    #タイマー差分
    def distance(self):
        return time.time() - self.setTime

    #タイマーリセット
    def reset(self):
        self.usedFlg = 0