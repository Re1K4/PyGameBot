#Manage numbers to control processing
import logging

logger = logging.getLogger(">")

NOW = 0
PREV = 0

def changeCtrl(ctrl):
    global NOW
    global PREV
    PREV = NOW
    NOW = ctrl
    logger.debug((f"ChangeControl [{PREV}] ⇒ [{NOW}]"))