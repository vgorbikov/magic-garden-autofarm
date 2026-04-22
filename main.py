from bot import GardenBot
import time  
from loguru import logger
import sys
from config import Config


config = Config.load_config('./config.yml')

bot = GardenBot(config)

time.sleep(2)
bot.calibrate()
bot.endless_harvesting()
# bot.shop_croops()
 
# import pygetwindow as gw   
# import pyautogui as ui

# b = gw.getWindowsWithTitle('Magic Garden')[0].box
 
# screen = ui.screenshot(region=b)
# screen.save('./screen_log/tst.png') 
