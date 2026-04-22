import time
import random
from enum import Enum
from PIL import Image
from typing import Any, Tuple

import pyautogui as ui
import pygetwindow as gw
from loguru import logger

from utils import Box

refs_path_prefix = './ui_refs'

SEARCH_STEP = 32

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


class ShopButton(Enum):
    UNKNOWN = 0
    BUY_BUTTON = 1
    OUT_OF_STOCK_BUTTON = 2


class ShopPosition(Enum):
    UNKNOWN = 0
    TULIP = 1
    CARROT = 2
    CACAO = 3
    SUNFLOWER = 4
    LYCHEE = 5
    DRAGON_FRUIT = 6
    CHRYSANTEMIUM = 7
    PEPPER = 8 
    PASSION_FRUIT = 9


BUTTON_REFS = {
    f'{refs_path_prefix}/HARVEST_DONATE_BUTTON.png': Button.HARVEST_DONATE,
    f'{refs_path_prefix}/HARVEST_BUTTON.png': Button.HARVEST_BASIC,
    f'{refs_path_prefix}/HARVEST_GOLD_BUTTON.png': Button.HARVEST_GOLG,
    f'{refs_path_prefix}/HARVEST_RAINBOW_BUTTON.png': Button.HARVEST_RAINBOW
}


SHOP_BUTTON_REFS = {
    f'{refs_path_prefix}/BUY_BUTTON_COIN.png': ShopButton.BUY_BUTTON,
    f'{refs_path_prefix}/OUT_OS_STOCK_BUTTON.png': ShopButton.OUT_OF_STOCK_BUTTON
}


SHOP_POSITION_REFS = {
    f'{refs_path_prefix}/TULIP_SEED_ON_SHOP.png': ShopPosition.TULIP,
    f'{refs_path_prefix}/CARROT_SEED_ON_SHOP.png': ShopPosition.CARROT,
    f'{refs_path_prefix}/CACAO_SEED_ON_SHOP.png': ShopPosition.CACAO,
    f'{refs_path_prefix}/CHRYSANTEMIUM_SEED_ON_SHOP.png': ShopPosition.CHRYSANTEMIUM,
    f'{refs_path_prefix}/DRAGON_FRUIT_SEED_ON_SHOP.png': ShopPosition.DRAGON_FRUIT,
    f'{refs_path_prefix}/LYCHEE_SEED_ON_SHOP.png': ShopPosition.LYCHEE,
    f'{refs_path_prefix}/SUNFLOWER_SEED_ON_SHOP.png': ShopPosition.SUNFLOWER
}


NOTIFICATION_REFS = {
    f'{refs_path_prefix}/FULL_INVENTORY_MSG.png': GameNotification.INVENTORY_FULL
}



def check_notification(region: Any, loc_callback: Any = None):
    for ref in NOTIFICATION_REFS.items():
        try:
            location = ui.locateOnScreen(
                ref[0], 
                confidence=0.6, 
                grayscale=False,
                step=SEARCH_STEP,
                region=region)
            logger.debug("Recognize {} notification", ref[1].name)
            return ref[1]
        except ui.ImageNotFoundException:
            pass 
    logger.debug("Recognize {} notification", GameNotification.UNKNOWN.name)
    return GameNotification.UNKNOWN
     

def check_button(region: Any, loc_callback: Any = None):
    screen = ui.screenshot(region=region)
    for ref in BUTTON_REFS.items():
        # n  = Image.open(ref[0])
        # print(screen.size)
        # print(n.size)
        try:
            location = ui.locateOnScreen(
                ref[0], 
                confidence=0.7, 
                grayscale=False,
                step=SEARCH_STEP,
                region=region)
            # log_screen = ui.screenshot(region=(int(location.left), int(location.top), int(location.width), int(location.height)))
            # log_screen.save(f'./screen_log/{ref[1].name}_button_{time.time()}.png')
            logger.debug("Recognize {} button", ref[1].name)
            if loc_callback:
                loc_callback(location)
                logger.debug("Button area is exact now to {}", location)
            return ref[1]
        except ui.ImageNotFoundException:
            pass 
    logger.debug("Recognize {} button", Button.UNKNOWN.name)
    return Button.UNKNOWN


def check_journal_warning_on_sell(region: Any):
    try:
        warn_loc = ui.locateOnScreen(
            f'{refs_path_prefix}/JOURNAL_WARNING.png', 
            confidence=0.6, 
            grayscale=False,
            step=SEARCH_STEP,
            region=region)
        return True
    except ui.ImageNotFoundException:
        return False


def check_shop_button(region: Any) -> Tuple[ShopButton, Box]:
    for ref in SHOP_BUTTON_REFS.items():
        try:
            button_loc = ui.locateCenterOnScreen(
                ref[0], 
                confidence=0.9, 
                grayscale=False,
                step=SEARCH_STEP,
                region=region)
            return ref[1], button_loc
        except ui.ImageNotFoundException:
            pass
    return ShopButton.UNKNOWN, ()


def check_shop_positions(region: Any):
    positions_loc = []
    for ref in SHOP_POSITION_REFS.items():
        try:
            button_loc = ui.locateCenterOnScreen(
                ref[0], 
                confidence=0.95, 
                grayscale=False,
                step=SEARCH_STEP,
                region=region)
            if button_loc:
                positions_loc.append((ref[1], button_loc))
        except ui.ImageNotFoundException:
            pass
    return positions_loc