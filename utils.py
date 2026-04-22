import random
import time
from typing import List, Tuple
from dataclasses import dataclass
from collections import namedtuple

import pygetwindow as gw

Box = namedtuple('Box', ['left', 'top', 'width', 'height'])

@dataclass(frozen=True)
class Point():
    x: int 
    y: int

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            x=d['x'],
            y=d['y']
        )
    
    def tuple(self) -> Tuple[int]:
        return (self.x, self.y)


@dataclass(frozen=True)
class LtRbBounds():
    lt: Tuple[int]
    rb: Tuple[int]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            lt=d['lt'],
            rb=d['rb']
        )


def randfloat(min: float = 0.05, max: float = 0.2):
    r = random.randint(1, 100)/100
    return min + (max-min)*r


def rand_delay(min: float = 0.05, max: float = 0.2):
    time.sleep(randfloat(min, max))


def get_window_position(win_title: str):
    wbox = gw.getWindowsWithTitle(win_title)[0].box
    wbox = tuple([(lambda x: x if x > 0 else 0)(c) for c in wbox])
    return Box(left=wbox[0], top=wbox[1], width=wbox[2], height=wbox[3])


def point_between_points_1d(point: int, a: int, b: int) -> bool:
    h_1 = point >= a and point <= b
    h_2 = point >= b and point <= a
    return h_1 or h_2

def check_point_in_bounds(point: Point, bounds: LtRbBounds):
    bx = point_between_points_1d(point.x, bounds.lt[0], bounds.rb[0])
    by = point_between_points_1d(point.y, bounds.lt[1], bounds.rb[1])
    return bx and by
