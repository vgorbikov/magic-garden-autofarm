import random
import time


def randfloat(min: float = 0.05, max: float = 0.2):
    r = random.randint(1, 100)/100
    return min + (max-min)*r


def rand_delay(min: float = 0.05, max: float = 0.2):
    time.sleep(randfloat(min, max))