import time

class Timer:
    def __init__(self):
        self.setTime = 0
        self.usedFlg = 0

    def set(self):
        if self.usedFlg == 0:
            self.setTime = time.time()
            self.usedFlg = 1

    def distance(self):
        return time.time() - self.setTime

    def reset(self):
        self.usedFlg = 0