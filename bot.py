import pyautogui as ui
import pydirectinput as di
import pygetwindow as gw
import time
import random
from enum import Enum
from collections import namedtuple

Box = namedtuple('Box', ['left', 'top', 'width', 'height'])

from utils import randfloat
from checks import check_button, check_notification, Button, GameNotification, check_journal_warning_on_sell

GARDEN_WIDTH = 21
GARDEN_HEIGHT = 10
EMPTY_X_INDEX = 10  #x-координата дорожки

START_POINT = (0, 0)

class Platform(Enum):
    DISCORD = 'Discord'



class GardenBot():
    def __init__(self, platform: Platform = Platform.DISCORD, start_point: tuple[int] = START_POINT):
        self._gamescreen_box = gw.getWindowsWithTitle(Platform.value)[0].box
        self._notification_area = Box(
            left = self._gamescreen_box.left,
            top = self._gamescreen_box.top,
            width = self._gamescreen_box.width,
            height = self._gamescreen_box.height//2)
        self._button_area = Box(
            left = self._gamescreen_box.left,
            top = self._gamescreen_box.top + self._gamescreen_box.height//2,
            width = self._gamescreen_box.width,
            height = self._gamescreen_box.height//2)
        self._start_point = start_point
        self._current_point = start_point

    def _long_press(self, key: str):
        di.keyDown(key)
        time.sleep(1.1)
        di.keyUp(key)

    def move_to(self, point: tuple[int]):
        dx = point[0] - self._current_point[0]
        dy = point[1] - self._current_point[1]

        x_key = 'left' if dx < 0 else 'right'
        y_key = 'up' if dy < 0 else 'down'

        di.press(y_key, interval=randfloat(0.05, 0.15), presses=abs(dy))
        di.press(x_key, interval=randfloat(0.05, 0.15), presses=abs(dx))

        self._current_point = (self._current_point[0] + dx, self._current_point[1] + dy)

    def harvest_croop(self) -> bool:
        button = check_button(self._button_area)
        if button in (Button.HARVEST_DONATE, Button.UNKNOWN):
            return False
        if button == Button.HARVEST_BASIC:
            di.press('space')
            return True
        if button in (Button.HARVEST_GOLG, Button.HARVEST_RAINBOW):
            self._long_press('space')
            return True
        
    def sell_croops(self):
        di.keyDown('shift')
        di.keyDown('3')
        time.sleep(0.05)
        di.keyUp('shift')
        di.keyUp('3')
        time.sleep(0.05)
        di.press('space')

        if check_journal_warning_on_sell(self._gamescreen_box):
            try:
                cnt = ui.locateCenterOnScreen(
                    './screens/JOURNAL_BUTTON.png', 
                    confidence=0.7, 
                    grayscale=False,
                    step=16,
                    region=self._gamescreen_box)
            except:
                screnshot = ui.screenshot(f'err_{time.time()}.png')
                screnshot.save(f'./screen_log/err_{time.time()}.png')

            ui.click(cnt.x, cnt.y)

            time.sleep(10)

            cnt = ui.locateCenterOnScreen(
                './screens/JOURNAL_CROSS.png', 
                confidence=0.7, 
                grayscale=False,
                step=16,
                region=self._gamescreen_box)

            ui.click(cnt.x, cnt.y)

            time.sleep(5)

            di.keyDown('shift')
            di.keyDown('3')
            time.sleep(0.05)
            di.keyUp('shift')
            di.keyUp('3')
            time.sleep(0.05)
            di.press('space')

        time.sleep(0.05)
        di.keyDown('shift')
        di.keyDown('2')
        time.sleep(0.05)
        di.keyUp('shift')
        di.keyUp('2')  
        time.sleep(0.05)

    def endless_harvesting(self):
        while True:
            for y in range(GARDEN_HEIGHT):
                for x in range(GARDEN_WIDTH):
                    self.move_to((x, y))

                    croop_available = True
                    while croop_available:
                        croop_available = self.harvest_croop()
                        notify = check_notification(self._notification_area)
                        if notify == GameNotification.INVENTORY_FULL:
                            self.sell_croops()
        