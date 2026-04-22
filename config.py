from dataclasses import dataclass
from turtle import position
from typing import List, Tuple
from enum import Enum

import yaml

from plants import Plants
from utils import Point, LtRbBounds


GARDEN_WIDTH = 21
GARDEN_HEIGHT = 10
EMPTY_X_INDEX = 10  #x-координата дорожки


class Platform(Enum):
    DISCORD = 'Discord'
    BROWSER = 'Magic Garden'


@dataclass(frozen=True)
class HarvestingConfig():
    active: bool 
    bounds: LtRbBounds
    exclude_areas: List[LtRbBounds | Tuple[int]]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            active=d['status'],
            bounds=LtRbBounds.from_dict(d['bounds']) if 'bounds' in d.keys() else None,
            exclude_areas=[(lambda x: LtRbBounds.from_dict(x) if type(x) == dict else Point(*x))(b) for b in d['exclude_areas']]
        )


@dataclass(frozen=True)
class MonitoredPosition():
    position: Plants 
    max_count: int 
    priority: int

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            position=d['position'],
            max_count=d['max_count'],
            priority=d['priority']
        )
        

@dataclass(frozen=True)
class ShoppingConfig():
    active: bool 
    monitored_positions: Tuple[MonitoredPosition]

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            active=d['status'],
            monitored_positions=[MonitoredPosition.from_dict(p) for p in d['monitored_positions']]
        )


@dataclass(frozen=True)
class Config():
    platform: Platform
    ui_lang: str
    start_position: Point
    harvest_conf: HarvestingConfig
    shopping_conf: ShoppingConfig

    @classmethod
    def load_config(cls: 'Config', path: str):
        with open(path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        return cls(
            platform=data['platform'],
            ui_lang=data['ui_lang'],
            start_position=Point(x=data['start_position']['x'], y=data['start_position']['y']),
            shopping_conf=ShoppingConfig.from_dict(data['instructions']['shopping']),
            harvest_conf=HarvestingConfig.from_dict(data['instructions']['harvesting'])
        )


