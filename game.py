import asyncio
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime
from uuid import uuid4
from enum import Enum

from jsonpatch import apply_patch
from playwright.async_api import WebSocketRoute

from ws_manager import WSManager
from log_manager import create_logger
from utils import ReprMixin
from config import Config



class Unknown(Enum):
    UNKNOWN = 'Unknown'


class ItemType(Enum):
    SEED = 'Seed'
    PET = 'Pet'
    PLANT = 'Plant'
    TOOL = 'Tool'
    DECOR = 'Decor'
    EGG = 'Egg'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Species(Enum):
    CARROT = 'Carrot'
    BEET = 'Beet'
    ECHEVERIA = 'Echeveria'
    CACTUS = 'Cactus'
    BAMBOO = 'Bamboo'
    SUNFLOWER = 'Sunflower'
    STARWEAVER = 'Starweaver'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class ToolId(Enum):
    WATERING_CAN = 'WateringCan'
    PLANTER_POT = 'PlanterPot'
    CROP_CLEANER = 'CropCleanser'
    SHOVEL = 'Shovel'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class DecorId(Enum):
    FEEDING_TROUGH = 'FeedingTrough'
    DECOR_SHED = 'DecorShed'
    PET_HUTCH = 'PetHutch'
    SEED_SILO = 'SeedSilo'
    TOOL_SHACK = 'ToolShack'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class EggId(Enum):
    COMMON = 'CommonEgg'
    UNCOMMON = 'UncommonEgg'
    RARE = 'RareEgg'
    LEGENDARY = 'LegendaryEgg'
    MYTHTICAL = 'MythicalEgg'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class PetSpecies(Enum):
    WORM = 'Worm'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN


class Shops(Enum):
    SEED = 'seed'
    EGG = 'egg'
    TOOL = 'tool'
    DECOR = 'decor'
    RAIN = 'rain'
    DAWN = 'dawn'
    AMBER = 'amber'
    SNOW = 'snow'
    THUNDER = 'thunder'
    UNKNOWN = 'Unknown'

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
    

class ShopPurchasePosition(ReprMixin):
    def __init__(self, raw_item_uid: Union[ToolId, EggId, Species, DecorId], count: int):
        self.__item_uid = raw_item_uid
        self.__count = count

    @property
    def uid(self) -> Union[ToolId, EggId, Species, DecorId]:
        if self.__item_uid in [t.value for t in ToolId]:
            return ToolId(self.__item_uid)
        if self.__item_uid in [t.value for t in EggId]:
            return EggId(self.__item_uid)
        if self.__item_uid in [t.value for t in Species]:
            return Species(self.__item_uid)
        if self.__item_uid in [t.value for t in DecorId]:
            return DecorId(self.__item_uid)
        return Unknown.UNKNOWN
    
    @property
    def cout(self) -> int:
        return int(self.__count)


class ShopPurchases(ReprMixin):
    def __init__(self, raw_purchases: Dict, raw_shop_name: str):
        self.__purchases: Dict = raw_purchases
        self.__shops = raw_shop_name

    @property
    def shopName(self) -> Shops:
        return Shops(self.__shops)

    @property
    def restockId(self) -> str:
        return self.__purchases["restockId"]
    
    @property
    def startedAtMs(self) -> int:
        return self.__purchases["startedAtMs"]
    
    @property
    def purchases(self) -> List[ShopPurchasePosition]:
        return [ShopPurchasePosition(p, c) for p, c in self.__purchases["purchases"].items()]


class AShopStock(ReprMixin):
    def __init__(self, raw_stock: Dict, current_user_purchases: ShopPurchases):
        self._stock: dict = raw_stock
        self.__current_user_purchases: ShopPurchases = current_user_purchases

    @property
    def itemType(self) -> Optional[ItemType]:
        if "itemType" in self._stock.keys():
            return ItemType(self._stock["itemType"])
        return None

    @property
    def initialStock(self) -> Optional[int]:
        if "initialStock" in self._stock.keys():
            return int(self._stock["initialStock"])
        return None
    
    @property
    def itemUName(self) -> Enum:
        pass

    @property
    def currentUserStock(self):
        if not self.__current_user_purchases:
            return self.initialStock
        this_item_filter = [p for p in self.__current_user_purchases.purchases if p.uid==self.itemUName]
        if len(this_item_filter)==0:
            return self.initialStock
        return self.initialStock - this_item_filter[0].cout


class SeedStock(AShopStock):
    @property
    def species(self) -> Species:
        if "species" in self._stock.keys():
            return Species(self._stock["species"])
        return None
    
    @property
    def itemUName(self) -> Species:
        return self.species


class ToolStock(AShopStock):
    @property
    def toolId(self) -> ToolId:
        if "toolId" in self._stock.keys():
            return Species(self._stock["toolId"])
        return None
    
    @property
    def itemUName(self) -> ToolId:
        return self.toolId


class EggStock(AShopStock):
    @property
    def eggId(self) -> EggId:
        if "eggId" in self._stock.keys():
            return Species(self._stock["eggId"])
        return None
    
    @property
    def itemUName(self) -> EggId:
        return self.eggId


class Shop(ReprMixin):
    def __init__(self, raw_shop: Dict, shop_name: Shops, current_user_purchases: ShopPurchases):
        self.__shop: Dict = raw_shop
        self.__shop_name: Shops = shop_name
        self.__current_user_purchases: ShopPurchases = current_user_purchases

    @property
    def shopName(self):
        return self.__shop_name

    @property
    def inventory(self) -> Optional[List[Union[SeedStock, ToolStock, EggStock]]]:
        if "inventory" in self.__shop.keys():
            all_items = self.__shop["inventory"]
            user_purchases = self.__current_user_purchases
            if self.restockId != self.__current_user_purchases.restockId:
                user_purchases = None
            seeds = [SeedStock(s, user_purchases) for s in all_items if s["itemType"]==ItemType.SEED.value]
            tools = [ToolStock(s, user_purchases) for s in all_items if s["itemType"]==ItemType.TOOL.value]
            eggs = [EggStock(s, user_purchases) for s in all_items if s["itemType"]==ItemType.EGG.value]
            return seeds + tools + eggs
        return None

    @property
    def startedAtMs(self) -> Optional[int]:
        if "startedAtMs" in self.__shop.keys():
            return self.__shop["startedAtMs"]
        return None

    @property
    def deadlineMs(self) -> Optional[int]:
        if "deadlineMs" in self.__shop.keys():
            return self.__shop["deadlineMs"]
        return None

    @property
    def restockId(self) -> Optional[str]:
        if "restockId" in self.__shop.keys():
            return self.__shop["restockId"]
        return None



class Item(ReprMixin):
    def __init__(self, raw_item: Dict):
        self._item: Dict = raw_item

    @property
    def itemType(self) -> ItemType:
        return ItemType(self._item["itemType"])
    
    @property
    def id(self) -> Optional[str]:
        if "id" in self._item.keys():
            return self._item["id"]


class PlantSlot(ReprMixin):
    def __init__(self, raw_slot: Dict):
        self.__slot: Dict = raw_slot

    @property
    def species(self) -> Optional[Species]:
        if "species" in self.__slot.keys():
            return Species(self.__slot["species"])
        return None
    
    @property
    def size(self) -> Optional[int]:
        if "size" in self.__slot.keys():
            return int(self.__slot["size"])
        return None
    
    @property
    def slotId(self) -> Optional[int]:
        if "slotId" in self.__slot.keys():
            return int(self.__slot["slotId"])
        return None
    
    @property
    def startTime(self) -> Optional[int]:
        if "startTime" in self.__slot.keys():
            return int(self.__slot["startTime"])
        return None
    
    @property
    def endTime(self) -> Optional[int]:
        if "endTime" in self.__slot.keys():
            return int(self.__slot["endTime"])
        return None


class Plant(Item):
    @property
    def species(self) -> Optional[Species]:
        if "species" in self._item.keys():
            return Species(self._item["species"])
        
    @property
    def slots(self) -> Optional[List[PlantSlot]]:
        if "slots" in self._item.keys():
            return [PlantSlot(s) for s in self._item["slots"]]
        return None
        

class Pet(Item):
    @property
    def petSpecies(self) -> PetSpecies:
        if "petSpecies" in self._item.keys():
            return PetSpecies(self._item["petSpecies"])
        return None
    
    @property
    def name(self) -> Optional[str]:
        if "name" in self._item.keys():
            return self._item["name"]
        return None
    
    @property
    def sourceEggId(self) -> EggId:
        if "sourceEggId" in self._item.keys():
            return EggId(self._item["sourceEggId"])
        return None
    
    @property
    def hunger(self) -> float:
        if "hunger" in self._item.keys():
            return float(self._item["hunger"])
        return None
    
    @property
    def xp(self) -> float:
        if "xp" in self._item.keys():
            return float(self._item["xp"])
        return None


class Storage(ReprMixin):
    def __init__(self, raw_storage: Dict):
        self.__storage: Dict = raw_storage

    @property
    def decorId(self) -> Optional[DecorId]:
        if "decorId" in self.__storage.keys():
            return self.__storage["decorId"]
        return None

    @property
    def capacitySlots(self) -> Optional[int]:
        if "capacitySlots" in self.__storage.keys():
            return self.__storage["capacitySlots"]
        return None

    @property
    def items(self) -> Optional[List[Union[Pet, Plant]]]:
        if "items" in self.__storage.keys():
            pets = [Pet(p) for p in self.__storage["items"] if p["itemType"]==ItemType.PET]
            plants = [Plant(p) for p in self.__storage["items"] if p["itemType"]==ItemType.PLANT]
            return pets + plants
        return None


class Player(ReprMixin):
    def __init__(self, raw_player: Dict, raw_slots: Dict):
        self.__player = raw_player
        self.__slots = raw_slots

    @property
    def id(self) -> Optional[str]:
        if "id" in self.__player.keys():
            return self.__player["id"]
        return None

    @property
    def name(self) -> str:
        if "name" in self.__player.keys():
            return self.__player["name"]
        return None

    @property
    def isConnected(self) -> bool:
        if "isConnected" in self.__player.keys():
            return self.__player["isConnected"]
        return None

    @property
    def inventory(self) -> List[Union[Plant, Pet]]:
        if "inventory" in self.__slots["data"].keys():
            if "items" in self.__slots["data"]["inventory"].keys():
                plants = [Plant(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.PLANT.value]
                pets = [Pet(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.PET.value]
                return plants + pets
            
        return None

    @property
    def storages(self) -> Storage:
        if "inventory" in self.__slots["data"].keys():
            if "storages" in self.__slots["data"]["inventory"].keys():
                return [Storage(s) for s in self.__slots["data"]["inventory"]["storages"]]
            
        return None

    @property
    def discordUserId(self) -> Optional[str]:
        if "discordUserId" in self.__player.keys():
            return self.__player["discordUserId"]
        return None 
    
    @property
    def shopPurchases(self) -> Optional[List[ShopPurchases]]:
        if "shopPurchases" in self.__slots["data"].keys():
            return [ShopPurchases(raw_purchases=purchases, raw_shop_name=shop_name) for shop_name, purchases in self.__slots["data"]["shopPurchases"].items()]
        return None


class GameState(ReprMixin):

    def __init__(self, raw_fullstate: Dict, current_user_name: str):
        self.__state = raw_fullstate
        self.__current_user_name: str = current_user_name

    def upd_state(self, json_patches: List[Dict]):
        apply_patch(self.__state, json_patches, in_place=True)

    def save_raw_state(self, path: str):
        with open(path, 'w') as f:
            f.write(json.dumps(self.__state, indent=4))
    
    @property
    def shops(self) -> Optional[List[Shop]]:
        if "shops" in self.__state["child"]["data"]:
            current_player_purchases = self.currentPlayer.shopPurchases
            shops = []
            for name, shop in self.__state["child"]["data"]["shops"].items():
                purchases = [p for p in current_player_purchases if p.shopName.value==name]
                if len(purchases) == 0:
                    purchases = None
                else:
                    purchases = purchases[0]
                shops.append(
                    Shop(
                        raw_shop=shop, 
                        shop_name=Shops(name),
                        current_user_purchases=purchases
                    )
                )
            return shops
        return None

    
    @property
    def hostPlayerId(self) -> Optional[str]:
        try:
            return self.__state["data"]["hostPlayerId"]
        except:
            return None
    
    @property
    def players(self) -> List[Player]:
        try:
            pairs = []
            players = [p for p in self.__state["data"]["players"] if p]
            slots = [s for s in self.__state["child"]["data"]["userSlots"] if s]
            for player in players:
                pairs.append((player, [s for s in slots if s["userId"]==player["id"]][0]))
            return [Player(raw_player=p[0], raw_slots=p[1]) for p in pairs]
        except:
            return None
        
    @property
    def currentPlayer(self) -> Optional[Player]:
        players_filter = [p for p in self.players if p.name==self.__current_user_name]
        if len(players_filter)==0:
            return None
        return players_filter[0]


class Command():
    def __init__(self, seq: int):
        self.requestId = str(uuid4())
        self.commandSequence = seq

    def __build_command(self):
        build = {
            "scopePath": [
                "Room",
                "Quinoa"
            ],
            "type": "QuinoaCommand",
            "requestId": self.requestId,
            "commandSequence": self.commandSequence,
            "command": {
                "type": "PurchaseShopItem",
                "shop": "seed",
                "viewMode": "grid",
                "item": {
                    "itemType": "Seed",
                    "species": "Carrot"
                }
            }
        }

    async def execute(self, server_ws, ):
        pass



class Game():
    def __init__(self, config: Config):
        self.state: GameState = None
        self.ws_manager: WSManager = None
        self.executed_command_sequence: int = 0
        self.config: Config = config

        self.logger, self.listener = create_logger(f'data/logs/game_log_{datetime.now().strftime("%d%m%Y_%H_%M_%S")}.log', "game")

    def __check_msg_is_typed(self, msg: Any) -> bool:
        try:
            msg = json.loads(msg)
        except json.JSONDecodeError:
            return False
        if isinstance(msg, dict):
            if "type" in msg.keys():
                return True
        return False
    
    def __decode_msg(self, msg: str) -> Dict:
        msg = json.loads(msg)
        return msg

    def set_ws_manager(self, manager: WSManager):
        self.ws_manager = manager
    
    def handle_server_msg(self, msg: str):
        if self.__check_msg_is_typed(msg):
            msg = self.__decode_msg(msg)
            self.logger.debug(f'[MSG HANDLED] type={msg["type"]}')
            if msg["type"] == "Welcome":
                self.state = GameState(msg["fullState"], self.config.auth.user_name)
            if msg["type"] == "RoomFrame":
                if "state" not in msg.keys():
                    pass
                else:
                    self.state.upd_state(msg["state"]["patches"])
            if "executedCommandSequence" in msg.keys():
                if msg["executedCommandSequence"] > self.executed_command_sequence:
                    self.executed_command_sequence = msg["executedCommandSequence"]

    def buy_seed(self, item: Species, count: int):
        command = {
            "scopePath": [
                "Room",
                "Quinoa"
            ],
            "type": "QuinoaCommand",
            "requestId": str(uuid4()),
            "commandSequence": self.executed_command_sequence+1,
            "command": {
                "type": "PurchaseShopItem",
                "shop": 'seed',
                "viewMode": "grid",
                "item": item.value,
                "quantity": count
            }
        }
        command = json.dumps(command)
        self.ws_manager.send_message_to_server(command, sender='BOT')

    async def loop_print_state(self):
        while True:
            if self.state:
                if self.state.shops:
                    print([s for s in self.state.shops if s.shopName==Shops.SEED])
                    print('-'*30)
            await asyncio.sleep(3)
