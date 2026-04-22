import pyautogui as ui
import pydirectinput as di
import pygetwindow as gw
import time
from enum import Enum
from loguru import logger

from config import Config, GARDEN_HEIGHT, GARDEN_WIDTH
from utils import Box, randfloat, get_window_position, check_point_in_bounds, Point
from checks import (check_button, check_notification, Button, 
                    GameNotification, check_journal_warning_on_sell, 
                    check_shop_button, check_shop_positions, 
                    ShopPosition, ShopButton)


refs_path_prefix = './ui_refs'



class GardenBot():
    def __init__(self, config: Config):
        self._config: Config = config
        # self._gamescreen_box = gw.getWindowsWithTitle(config.platform)[0].box
        self._gamescreen_box = get_window_position(config.platform)

        # gamescreen_shot = ui.screenshot(region=self._gamescreen_box)
        # gamescreen_shot.save('./screen_log/game_screen.png')
        # logger.debug("Finds a game window at {}; Screenshot saved", self._gamescreen_box)

        logger.debug("Configured bounds: {}", self._config.harvest_conf.bounds)
        logger.debug("Configured excluded areas: {}", self._config.harvest_conf.exclude_areas)

        self._screen_center = (self._gamescreen_box.left + self._gamescreen_box.width//2,
                               self._gamescreen_box.top + self._gamescreen_box.height//2)
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
        # gamescreen_shot = ui.screenshot(region=self._button_area)
        # gamescreen_shot.save('./screen_log/button_area_screen.png')
        # logger.debug("Screenshot of button area saved", self._gamescreen_box)

        self._button_area_is_exact: bool = False
        self._current_point = self._config.start_position.tuple()

    def _now_in_excluded_area(self) -> bool:
        '''
        Check if there is a bot in the excluded area
        '''
        ex_areas = self._config.harvest_conf.exclude_areas
        if ex_areas is None:
            return False
        cur_point = Point(self._current_point[0], self._current_point[1])
        for ex_area in ex_areas:
            if isinstance(ex_area, Point):
                if cur_point == ex_area:
                    return True
                else:
                    continue
            if check_point_in_bounds(cur_point, ex_area):
                return True
        return False

    def _long_press(self, key: str):
        di.keyDown(key)
        time.sleep(1.1)
        di.keyUp(key)


    def exact_button_area(self, loc: Box):
        a_px = 100
        self._button_area = Box(
            left=int(loc.left-a_px),
            top=int(loc.top-a_px),
            width=int(loc.width+2*a_px),
            height=int(loc.height+2*a_px)
        )
        self._button_area_is_exact = True


    def calibrate(self):
        logger.info("Calibrate starts...")
        for i in range(2):
            for j in range(3):
                self.move_to((i, j))
                button = check_button(self._button_area, self.exact_button_area)
        self.move_to(self._config.start_position.tuple())
        logger.info("Calibrate done! OK?")


    def move_to(self, point: tuple[int]):
        dx = point[0] - self._current_point[0]
        dy = point[1] - self._current_point[1]

        x_key = 'left' if dx < 0 else 'right'
        y_key = 'up' if dy < 0 else 'down'

        di.press(y_key, interval=randfloat(0.02, 0.08), presses=abs(dy))
        di.press(x_key, interval=randfloat(0.02, 0.08), presses=abs(dx))

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
                    f'{refs_path_prefix}/JOURNAL_BUTTON.png', 
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
                f'{refs_path_prefix}/JOURNAL_CROSS.png', 
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
        harv_check_limit = 10

        if self._config.harvest_conf.bounds is None:
            lt_point = (0, 0)
            rb_point = (GARDEN_WIDTH-1, GARDEN_HEIGHT-1)
        else:
            lt_point = self._config.harvest_conf.bounds.lt
            rb_point = self._config.harvest_conf.bounds.rb

        self.move_to(lt_point)
      
        while True:
            for y in range(lt_point[1], rb_point[1]+1):
                xrange = range(lt_point[0], rb_point[0]+1) if y%2 == 0 else range(rb_point[0], lt_point[0]-1, -1)
                for x in xrange:
                    self.move_to((x, y))
                    if self._now_in_excluded_area():
                        logger.debug("Now bot in EXCLUDED AREA {} -> skip harvesting there", self._current_point)
                        continue

                    croop_available = True
                    while croop_available:
                        croop_available = self.harvest_croop()
                        harv_check_limit -= 1
                        if harv_check_limit <= 0:
                            harv_check_limit = 10
                            notify = check_notification(self._notification_area)
                            if notify == GameNotification.INVENTORY_FULL:
                                self.sell_croops()
        
            time.sleep(1)

    def shop_croop(self, max_count: int = 30) -> int:
        but = check_shop_button(self._gamescreen_box)
        logger.debug("Recognize {} in shop", but[0])
        count = 0
        while but[0] == ShopButton.BUY_BUTTON and count < max_count:
            ui.click(but[1])
            count += 1
            but = check_shop_button(self._gamescreen_box)

    def shop_croops(self):
        di.keyDown('shift')
        di.keyDown('1')
        time.sleep(0.05)
        di.keyUp('shift')
        di.keyUp('1')
        time.sleep(0.05)
        di.press('space')

        di.moveTo(self._screen_center[0], self._screen_center[1])

        for i in range(100):
            locs = check_shop_positions(self._gamescreen_box)
            for loc in locs:
                logger.debug("Finds something wrong...")
                if loc[0] == ShopPosition.TULIP:
                    logger.debug("Finds {}", loc[0])
                    ui.click(loc[1])
                    time.sleep(0.5)
                    self.shop_croop(3)
                    return
            ui.scroll(-150)
            logger.debug("Scroll 150 to down")

        