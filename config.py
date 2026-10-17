from dataclasses import dataclass
from pathlib import Path
from typing import Union, List, Optional

import yaml

from game.game_types import ToolId, EggId, Species, Shops, Unknown



@dataclass
class ShopItemsDirectiveTarget():
    shop: Shops
    item: Union[ToolId, EggId, Species]
    item_limit: Optional[int] = None

    def __post_init__(self):
        if self.item_limit and not isinstance(self.item_limit, int):
            self.item_limit = int(self.item_limit)
        if not isinstance(self.shop, Shops):
            self.shop = Shops(self.shop)
        if not isinstance(self.item, (ToolId, EggId, Species)):
            if self.item in [m.value for m in ToolId]:
                self.item = ToolId(self.item)
            elif self.item in [m.value for m in EggId]:
                self.item = EggId(self.item)
            elif self.item in [m.value for m in Species]:
                self.item = Species(self.item)
            else:
                self.item = Unknown.UNKNOWN


@dataclass
class ShopItemsDirectiveConf():
    status: bool 
    targets: List[ShopItemsDirectiveTarget]

    def __post_init__(self):
        if not isinstance(self.status, bool):
            self.status = bool(self.on)
        if not isinstance(self.targets[0], ShopItemsDirectiveTarget):
            self.targets = [ShopItemsDirectiveTarget(**t) for t in self.targets]


@dataclass
class PetTeamDefinition():
    team_name: str


@dataclass
class SituationshipTeamsConf():
    on_sell_crops: PetTeamDefinition
    on_harvest: PetTeamDefinition
    on_sell_pets: PetTeamDefinition

    def __post_init__(self):
        if not isinstance(self.on_sell_crops, PetTeamDefinition):
            self.on_sell_crops = PetTeamDefinition(**self.on_sell_crops)
        if not isinstance(self.on_harvest, PetTeamDefinition):
            self.on_harvest = PetTeamDefinition(**self.on_harvest)
        if not isinstance(self.on_sell_pets, PetTeamDefinition):
            self.on_sell_pets = PetTeamDefinition(**self.on_sell_pets)


@dataclass
class WeatherTeamsConf():
    rain: Optional[PetTeamDefinition] = None
    snow: Optional[PetTeamDefinition] = None
    thunder: Optional[PetTeamDefinition] = None
    amber: Optional[PetTeamDefinition] = None
    dawn: Optional[PetTeamDefinition] = None
    default_team: Optional[PetTeamDefinition] = None

    def __post_init__(self):
        if self.rain and not isinstance(self.rain, PetTeamDefinition):
            self.rain = PetTeamDefinition(**self.rain)
        if self.snow and not isinstance(self.snow, PetTeamDefinition):
            self.snow = PetTeamDefinition(**self.snow)
        if self.thunder and not isinstance(self.thunder, PetTeamDefinition):
            self.thunder = PetTeamDefinition(**self.thunder)
        if self.amber and not isinstance(self.amber, PetTeamDefinition):
            self.amber = PetTeamDefinition(**self.amber)
        if self.dawn and not isinstance(self.dawn, PetTeamDefinition):
            self.dawn = PetTeamDefinition(**self.dawn)
        if self.default_team and not isinstance(self.default_team, PetTeamDefinition):
            self.default_team = PetTeamDefinition(**self.default_team)


@dataclass
class WeatherPetTeamRotationDirectiveConf():
    status: bool 
    weather_teams: WeatherTeamsConf

    def __post_init__(self):
        if not isinstance(self.weather_teams, WeatherTeamsConf):
            self.weather_teams = WeatherTeamsConf(**self.weather_teams)


@dataclass
class SituationshipPetRotationDirectiveConf():
    status: bool 
    situationship_teams: SituationshipTeamsConf

    def __post_init__(self):
        if not isinstance(self.situationship_teams, SituationshipTeamsConf):
            self.situationship_teams = SituationshipTeamsConf(**self.situationship_teams)


@dataclass
class DirectivesConf():
    shop_items: ShopItemsDirectiveConf
    weather_pet_teams_rotation: WeatherPetTeamRotationDirectiveConf
    situationsip_pet_team_rotation: SituationshipPetRotationDirectiveConf

    def __post_init__(self):
        if not isinstance(self.shop_items, ShopItemsDirectiveConf):
            self.shop_items = ShopItemsDirectiveConf(**self.shop_items)
        if not isinstance(self.weather_pet_teams_rotation, WeatherPetTeamRotationDirectiveConf):
            self.weather_pet_teams_rotation = WeatherPetTeamRotationDirectiveConf(**self.weather_pet_teams_rotation)
        if not isinstance(self.situationsip_pet_team_rotation, SituationshipPetRotationDirectiveConf):
            self.situationsip_pet_team_rotation = SituationshipPetRotationDirectiveConf(**self.situationsip_pet_team_rotation)


@dataclass
class AuthConfig():
    user_name: str
    saved_auth_state_path: Path

    def __post_init__(self):
        self.saved_auth_state_path = Path(self.saved_auth_state_path)


@dataclass
class Config():
    auth: AuthConfig
    directives: DirectivesConf

    def __post_init__(self):
        if not isinstance(self.auth, AuthConfig):
            self.auth = AuthConfig(**self.auth)
        if not isinstance(self.directives, DirectivesConf):
            self.directives = DirectivesConf(**self.directives)
    
    @classmethod
    def loads_from_yaml(cls, path: Union[Path, str]):
        if isinstance(path, Path):
            path = path.as_posix()
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return cls(**config)
