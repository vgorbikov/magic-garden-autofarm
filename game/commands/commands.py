from dataclasses import dataclass
from typing import Optional, Union, Dict, Tuple

from game import commands
from game.game_types import CommandType, Species, ToolId, EggId, DecorId, ItemType, Shops
from game.commands.base import ACommand, ACommandResult



@dataclass
class PurchaseShopItemResult(ACommandResult):
    itemGains: str = ''
    commandType: CommandType = CommandType.PURCHASE_SHOP_ITEM


class PurchaseShopItem(ACommand):
    def __init__(self, shop: Shops, itemType: ItemType, item: Union[ToolId, EggId, Species], count: int = 1):
        super().__init__(CommandType.PURCHASE_SHOP_ITEM, PurchaseShopItemResult)
        self.shop = shop
        self.item_type = itemType
        self.item = item
        self.count = count

    def _build_command(self):
        item_specs = {
            ToolId: "toolId",
            EggId: "eggId",
            Species: "species",
            DecorId: "decorId"
        }
        command =  {
            "type": self.comand_type.value,
            "shop": self.shop.value,
            "viewMode": "grid",
            "item": {
                "itemType": self.item_type.value,
                item_specs[type(self.item)]: self.item.value
            },
            "quantity": self.count
        }
        return command
    
@dataclass
class ApplyPetTeamResult(ACommandResult):
    commandType: CommandType = CommandType.APPLY_PET_TEAM


class ApplyPetTeam(ACommand):
    def __init__(self, teamId: str):
        super().__init__(CommandType.APPLY_PET_TEAM, ApplyPetTeamResult)
        self.team_id = teamId

    def _build_command(self):
        command = {
            "type": self.comand_type.value,
            "teamId": self.team_id
        }
        return command
    

@dataclass
class HarvestCropResult(ACommandResult):
    itemGains: str = ''
    commandType = CommandType.HARVEST_CROP


class HarvestCrop(ACommand):
    def __init__(self, slot: int, slotIndex: int, cropItemId: str):
        super().__init__(CommandType.HARVEST_CROP, HarvestCropResult)
        self.slot = slot
        self.slotIndex = slotIndex
        self.crop_item_id = cropItemId


    def _build_command(self):
        command = {
            "type": self.comand_type.value,
            "slot": self.slot,
            "slotsIndex": self.slotIndex,
            "cropItemId": self.crop_item_id
        }
        return command


@dataclass
class FeedPetResult(ACommandResult):
    commandType = CommandType.FEED_PET


class FeedPet(ACommand):
    def __init__(self, pet_item_id: str, crop_item_id: str):
        super().__init__(CommandType.FEED_PET, FeedPetResult)
        self.pet_id = pet_item_id
        self.crop_item_id = crop_item_id

    def _build_command(self):
        command = {
            "type": self.comand_type.value,
            "petItemId": self.pet_id,
            "cropItemId": self.crop_item_id
        }
        return command


@dataclass
class GrowEggResult(ACommandResult):
    commandType = CommandType.GROW_EGG


class GrowEgg(ACommand):
    def __init__(self, slot: int, egg_id: EggId):
        super().__init__(CommandType.GROW_EGG, GrowEggResult)
        self.slot = slot 
        self.egg_id = egg_id

    def _build_command(self) -> Dict:
        command = {
            "type": self.comand_type.value,
            "slot": self.slot,
            "eggId": self.egg_id.value
        }
        return command


@dataclass
class HatchEggResult(ACommandResult):
    commandType = CommandType.HATCH_EGG

class HatchEgg(ACommand):
    def __init__(self, slot: int):
        super().__init__(CommandType.HATCH_EGG, HatchEggResult)
        self.slot = slot

    def _build_command(self):
        return {
            "type": self.comand_type.value,
            "slot": self.slot
        }


@dataclass
class SellPetResult(ACommandResult):
    commandType = CommandType.SELL_PET
    currencyGains: str = ''


class SellPet(ACommand):
    def __init__(self, item_id: str):
        super().__init__(CommandType.SELL_PET, SellPetResult)
        self.item_id = item_id

    def _build_command(self):
        return {
            "type": self.comand_type.value,
            "itemId": self.item_id
        }
