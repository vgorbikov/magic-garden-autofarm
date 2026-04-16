import pyautogui as ui
import pydirectinput as di
import pygetwindow as gw
import time
import random


screen_width, screen_height = ui.size()

mg_area = gw.getWindowsWithTitle('Discord')[0]


garden_width = 6
garden_height = 6
taps_max = 2
harvest_pause_time = 180


def randtime(min: float = 0.05, max: float = 0.2):
    r = random.randint(1, 100)/100
    return min + (max-min)*r


def press(key: str):
    di.press(key) 
    # timesleep = randtime(0.01, 0.1)
    # time.sleep(timesleep)  


def long_press(key: str, duration_sec: float):
    di.keyDown(key)
    time.sleep(duration_sec)
    di.keyUp(key)


class Garden():
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.current_position_x: int = self.width-1
        self.current_position_y: int = 0

    def move(self, x: int, y: int):
        self.current_position_x += x
        self.current_position_y += y

    def get_current_position(self):
        return(self.current_position_x, self.current_position_y)
    

garden = Garden(garden_width, garden_height)
start_p = garden.get_current_position()

def check_croop_type():
    los_step = 16
    try:
        golden_croop = ui.locateOnScreen(
        './screens/HARVEST_DONATE_BUTTON.png', 
        confidence=0.7, 
        grayscale=False,
        step=los_step,
        region=mg_area.box)
        return 'green'
    except ui.ImageNotFoundException:
        pass 

    try:
        golden_croop = ui.locateOnScreen(
        './screens/HARVEST_GOLD_BUTTON.png', 
        confidence=0.7, 
        grayscale=False,
        step=los_step,
        region=mg_area.box)
        return 'gold'
    except ui.ImageNotFoundException:
        pass 

    try:
        golden_croop = ui.locateOnScreen(
        './screens/HARVEST_RAINBOW_BUTTON.png', 
        confidence=0.7, 
        grayscale=False,
        step=los_step,
        region=mg_area.box)
        return 'rainbow'
    except ui.ImageNotFoundException:
        pass 

    return 'standard'


def harvest_croop():
    croop_type = check_croop_type()

    while croop_type != 'green':
        if croop_type == 'gold' or croop_type == 'rainbow':
            long_press('space', 1.5)
            print(f'Hravest {croop_type} croop!')
        else:
            press('space')
        croop_type = check_croop_type()


def harvest():
    print('Harvesting...')
    for i in range(garden.height):
        cur_p = garden.get_current_position()
        lit = 'left' if cur_p[0] >= garden.width-1 else 'right'
        move_x = -1 if lit == 'left' else 1
        for i in range(garden.width-1):
            harvest_croop()
            press(lit)
            garden.move(move_x, 0)
        else:
            harvest_croop()
        if cur_p[1] < garden.height-1:
            press('down')
            garden.move(0, 1)

def check_sell_journal_warning() -> bool:
    try:
        golden_croop = ui.locateOnScreen(
        './screens/JOURNAL_WARNING.png', 
        confidence=0.7, 
        grayscale=False,
        step=16,
        region=mg_area.box)
        return True
    except ui.ImageNotFoundException:
        return False

def to_start():
    print('Go to start')
    cur_p = garden.get_current_position()
    move_x = start_p[0] - cur_p[0]
    move_y = start_p[1] - cur_p[1]

    lit_x = 'left' if move_x < 0 else 'right'
    lit_y = 'up' if move_y < 0 else 'down'

    for i in range(abs(move_x)):
        press(lit_x)
        timesleep = randtime(0.01, 0.1)
        time.sleep(timesleep)  

    for i in range(abs(move_y)):
        press(lit_y)
        timesleep = randtime(0.01, 0.1)
        time.sleep(timesleep) 
    
    garden.move(move_x, move_y)   

def sell():
    print('Selling all...')
    di.keyDown('shift')
    di.keyDown('3')
    time.sleep(0.05)
    di.keyUp('shift')
    di.keyUp('3')
    time.sleep(0.05)
    di.press('space')

    if check_sell_journal_warning():
        print('We have JOURNAL INCIDENT (!)')
        try:
            cnt = ui.locateCenterOnScreen(
            './screens/JOURNAL_BUTTON.png', 
            confidence=0.7, 
            grayscale=False,
            step=16,
            region=mg_area.box)
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
        region=mg_area.box)

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
    print('Selling all!')

def waiting(seconds: int):
    print(f'Waiting {seconds} second')
    start_time = time.time()# @#
    while time.time() - start_time < seconds:
        press('left')
        time.sleep(randtime(1, 2))
        press('right')
        time.sleep(randtime(1, 2))

time.sleep(5)
while True:         
    harvest()
    to_start()
    sell()
    # waiting(harvest_pause_time) 
