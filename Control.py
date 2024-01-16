import logging

logger = logging.getLogger(">")

#現在の制御番号
NOW = 0
#一つ前の制御番号
PREV = 0

def changeCtrl(ctrl):
    global NOW
    global PREV
    PREV = NOW
    NOW = ctrl
    logger.debug((f"ChangeControl [{PREV}] ⇒ [{NOW}]"))