import time
import random
from enum import Enum
from typing import Any

import pyautogui as ui
import pygetwindow as gw



class Button(Enum):
    '''
    Button types enum
    '''
    UNKNOWN = 1
    HARVEST_BASIC = 2
    HARVEST_RAINBOW = 3
    HARVEST_GOLG = 4
    HARVEST_DONATE = 5



class GameNotification(Enum):
    '''
    Notification types enum
    '''
    UNKNOWN = 1
    INVENTORY_FULL = 2



BUTTON_REFS = {
    './screens/HARVEST_DONATE_BUTTON.png': Button.HARVEST_DONATE,
    './screens/HARVEST_BUTTON.png': Button.HARVEST_BASIC,
    './screens/HARVEST_GOLD_BUTTON.png': Button.HARVEST_GOLG,
    './screens/HARVEST_RAINBOW_BUTTON.png': Button.HARVEST_RAINBOW
}

NOTIFICATION_REFS = {
    './screens/FULL_INVENTORY_MSG.png': GameNotification.INVENTORY_FULL
}



def check_notification(region: Any):
    for ref in NOTIFICATION_REFS.items():
        try:
            location = ui.locateOnScreen(
                ref[0], 
                confidence=0.7, 
                grayscale=False,
                step=16,
                region=region)
            return ref[1]
        except ui.ImageNotFoundException:
            pass 
    return GameNotification.UNKNOWN
     


def check_button(region: Any):
    for ref in BUTTON_REFS.items():
        try:
            location = ui.locateOnScreen(
                ref[0], 
                confidence=0.7, 
                grayscale=False,
                step=16,
                region=region)
            return ref[1]
        except ui.ImageNotFoundException:
            pass 
    return Button.UNKNOWN


def check_journal_warning_on_sell(region: Any):
    try:
        warn_loc = ui.locateOnScreen(
            './screens/JOURNAL_WARNING.png', 
            confidence=0.7, 
            grayscale=False,
            step=16,
            region=region)
        return True
    except ui.ImageNotFoundException:
        return False
