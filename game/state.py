import json
from typing import Dict, List, Any, Optional, Union
from enum import Enum, member
import asyncio
import inspect

from jsonpatch import apply_patch

from utils import ReprMixin
from ws_manager import WSManager
from game.game_types import ToolId, EggId, Species, PetSpecies, DecorId, Unknown, Shops, ItemType, Weather, ObjectType



class ShopPurchasePosition(ReprMixin):
    def __init__(self, raw_item_uid: Union[ToolId, EggId, Species, DecorId], count: int):
        self.__item_uid = raw_item_uid
        self.__count = count

    @property
    def itemUName(self) -> Union[ToolId, EggId, Species, DecorId]:
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
    def count(self) -> int:
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


class Item(ReprMixin):
    def __init__(self, raw_item: Dict, **kwargs):
        self._item: Dict = raw_item

    @property
    def itemType(self) -> Optional[ItemType]:
        if "itemType" in self._item.keys():
            return ItemType(self._item["itemType"])
        return None
    
    @property
    def itemUName(self) -> Union[Species, ToolId, DecorId, EggId]:
        pass


class AShopItem(Item):
    def __init__(self, current_user_purchases: ShopPurchases, **kwargs):
        super().__init__(**kwargs)
        self.__current_user_purchases: ShopPurchases = current_user_purchases

    @property
    def initialStock(self) -> Optional[int]:
        if "initialStock" in self._item.keys():
            return int(self._item["initialStock"])
        return None

    @property
    def currentUserStock(self):
        if not self.__current_user_purchases:
            return self.initialStock
        this_item_filter = [p for p in self.__current_user_purchases.purchases if p.itemUName==self.itemUName]
        if len(this_item_filter)==0:
            return self.initialStock
        return self.initialStock - this_item_filter[0].count


class Seed(Item):
    @property
    def species(self) -> Species:
        if "species" in self._item.keys():
            return Species(self._item["species"])
        return None
    
    @property
    def itemUName(self) -> Species:
        return self.species
    

class Tool(Item):
    @property
    def toolId(self) -> ToolId:
        if "toolId" in self._item.keys():
            return ToolId(self._item["toolId"])
        return None
    
    @property
    def itemUName(self) -> ToolId:
        return self.toolId
    

class Egg(Item):
    @property
    def eggId(self) -> EggId:
        if "eggId" in self._item.keys():
            return EggId(self._item["eggId"])
        return None
    
    @property
    def itemUName(self) -> EggId:
        return self.eggId
    
class EggInInventory(Egg):
    @property
    def quantity(self) -> Optional[int]:
        if "quantity" in self._item.keys():
            return int(self._item["quantity"])
        return None


class SeedInShop(Seed, AShopItem):
    def __init__(self, raw_item: Dict, current_user_purchases: ShopPurchases):
        super().__init__(raw_item=raw_item, current_user_purchases=current_user_purchases)


class SeedInInventory(Seed):
    @property
    def quantity(self) -> Optional[int]:
        if "quantity" in self._item.keys():
            return int(self._item["quantity"])
        return None


class ToolInInventory(Tool):
    @property
    def quantity(self) -> Optional[int]:
        if "quantity" in self._item.keys():
            return int(self._item["quantity"])
        return None
    

class RemainedTool(Tool):
    @property
    def remainingActiveSeconds(self) -> Optional[int]:
        if "remainingActiveSeconds" in self._item.keys():
            return int(self._item["remainingActiveSeconds"])
        return None


class RemainedToolInInventory(ToolInInventory, RemainedTool):
    pass


class ToolInShop(Tool, AShopItem):
    def __init__(self, raw_item: Dict, current_user_purchases: ShopPurchases):
        super().__init__(raw_item=raw_item, current_user_purchases=current_user_purchases)


class EggInShop(Egg, AShopItem):
    def __init__(self, raw_item: Dict, current_user_purchases: ShopPurchases):
        super().__init__(raw_item=raw_item, current_user_purchases=current_user_purchases)


class Shop(ReprMixin):
    def __init__(self, raw_shop: Dict, shop_name: Shops, current_user_purchases: ShopPurchases):
        self.__shop: Dict = raw_shop
        self.__shop_name: Shops = shop_name
        self.__current_user_purchases: ShopPurchases = current_user_purchases

    @property
    def shopName(self):
        return self.__shop_name

    @property
    def inventory(self) -> Optional[List[Union[SeedInShop, ToolInShop, EggInShop]]]:
        if "inventory" in self.__shop.keys():
            all_items = self.__shop["inventory"]
            user_purchases = self.__current_user_purchases
            if self.restockId != self.__current_user_purchases.restockId:
                user_purchases = None
            seeds = [SeedInShop(s, user_purchases) for s in all_items if s["itemType"]==ItemType.SEED.value]
            tools = [ToolInShop(s, user_purchases) for s in all_items if s["itemType"]==ItemType.TOOL.value]
            eggs = [EggInShop(s, user_purchases) for s in all_items if s["itemType"]==ItemType.EGG.value]
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



class ItemWithId(Item):
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



class MGObject(ReprMixin):
    def __init__(self, raw_object: Dict):
        self._object = raw_object

    @property
    def objectType(self):
        if "objectType" in self._object.keys():
            return ObjectType(self._object["objectType"])



class PlantItem(ItemWithId):
    @property
    def species(self) -> Optional[Species]:
        if "species" in self._item.keys():
            return Species(self._item["species"])
        
    @property
    def slots(self) -> Optional[List[PlantSlot]]:
        if "slots" in self._item.keys():
            return [PlantSlot(s) for s in self._item["slots"]]
        return None
    

class PlantObject(MGObject):
    @property
    def species(self) -> Optional[Species]:
        if "species" in self._object.keys():
            return Species(self._object["species"])
        
    @property
    def slots(self) -> Optional[List[PlantSlot]]:
        if "slots" in self._object.keys():
            return [PlantSlot(s) for s in self._object["slots"]]
        return None
        

class EggObject(MGObject):
    @property
    def eggId(self) -> EggId:
        if "eggId" in self._object.keys():
            return EggId(self._object["eggId"])

    @property
    def plantedAt(self) -> int:
        if "plantedAt" in self._object.keys():
            return int(self._object["plantedAt"])
    
    @property
    def maturedAt(self) -> int:
        if "maturedAt" in self._object.keys():
            return int(self._object["maturedAt"])


class Pet(ItemWithId):
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
    

class PetTeamMember(ReprMixin):
    def __init__(self, raw_member: Dict):
        self._member: Dict = raw_member

    @property
    def petId(self) -> str:
        return self._member["petId"]
    
    @property
    def petSpecies(self) -> PetSpecies:
        return PetSpecies(self._member["petSpecies"])
    
    @property
    def name(self) -> Optional[str]:
        return self._member["name"]
    

class PetTeam(ReprMixin):
    def __init__(self, raw_team: Dict):
        self._team: Dict = raw_team

    @property
    def id(self) -> str:
        return self._team["id"]
    
    @property
    def name(self) -> Optional[str]:
        return self._team["name"]
    
    @property
    def members(self) -> List[PetTeamMember]:
        return [PetTeamMember(m) for m in self._team["members"]]


class Produce(ItemWithId):
    @property
    def itemType(self) -> ItemType:
        return ItemType.PRODUCE
    
    @property
    def size(self) -> int:
        if "size" in self._item.keys():
            return int(self._item["size"])
        
    @property
    def species(self) -> Species:
        if "species" in self._item.keys():
            return Species(self._item["species"])

    @property 
    def itemUName(self) -> Species:
        return self.species


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
    def items(self) -> Optional[List[Union[Pet, PlantItem, SeedInInventory, ToolInInventory, RemainedToolInInventory, EggInInventory]]]:
        if "items" in self.__storage.keys():
            pets = [Pet(p) for p in self.__storage["items"] if p["itemType"]==ItemType.PET.value]
            plants = [PlantItem(p) for p in self.__storage["items"] if p["itemType"]==ItemType.PLANT.value]
            seeds = [SeedInInventory(s) for s in self.__storage["items"] if s["itemType"]==ItemType.SEED.value]
            eggs = [EggInInventory(s) for s in self.__storage["items"] if s["itemType"]==ItemType.EGG.value]
            tools = [ToolInInventory(p) for p in self.__storage["items"] if p["itemType"]==ItemType.TOOL.value and "remainingActiveSeconds" not in p.keys()]
            remained_tools = [RemainedToolInInventory(p) for p in self.__storage["items"] if p["itemType"]==ItemType.TOOL.value and "remainingActiveSeconds" in p.keys()]
            return pets + plants + seeds + tools + remained_tools + eggs
        return None


class Tile(ReprMixin):
    def __init__(self, tile_no: int, raw_tile: Dict):
        self.__tine_no = tile_no
        self.__tile = raw_tile

    @property
    def tile_no(self) -> int:
        return self.__tine_no
    
    @property
    def object_in_tile(self) -> Union[EggObject, PlantObject, None]:
        if self.__tile is None:
            return None
        obj_type = ObjectType(self.__tile["objectType"])
        if obj_type == ObjectType.PLANT:
            return PlantObject(self.__tile)
        if obj_type == ObjectType.EGG:
            return EggObject(self.__tile)
        return MGObject(self.__tile)


class Garden(ReprMixin):
    def __init__(self, raw_garden: Dict):
        self.__garden = raw_garden

    @property
    def gardenTiles(self) -> List[Tile]:
        if "tileObjects" in self.__garden.keys():
            tiles_dict = self.__garden["tileObjects"]
            raw_tiles = {i:tiles_dict[str(i)] if str(i) in tiles_dict.keys() else None for i in range(200)}
            return [Tile(int(i[0]), i[1]) for i in raw_tiles.items()]


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
    def garden(self) -> Garden:
        if "garden" in self.__slots["data"].keys():
            return Garden(self.__slots["data"]["garden"])

    @property
    def inventory(self) -> List[Union[PlantItem, Pet, SeedInInventory, ToolInInventory, RemainedToolInInventory, EggInInventory, Produce]]:
        if "inventory" in self.__slots["data"].keys():
            if "items" in self.__slots["data"]["inventory"].keys():
                pets = [Pet(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.PET.value]
                plants = [PlantItem(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.PLANT.value]
                seeds = [SeedInInventory(s) for s in self.__slots["data"]["inventory"]["items"] if s["itemType"]==ItemType.SEED.value]
                eggs = [EggInInventory(s) for s in self.__slots["data"]["inventory"]["items"] if s["itemType"]==ItemType.EGG.value]
                tools = [ToolInInventory(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.TOOL.value and "remainingActiveSeconds" not in p.keys()]
                remained_tools = [RemainedToolInInventory(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.TOOL.value and "remainingActiveSeconds" in p.keys()]
                produce = [Produce(p) for p in self.__slots["data"]["inventory"]["items"] if p["itemType"]==ItemType.PRODUCE.value]
                return plants + pets + seeds + tools + remained_tools + eggs + produce
            
        return None

    @property
    def storages(self) -> List[Storage]:
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
    
    @property
    def petTeams(self) -> List[PetTeam]:
        return [PetTeam(t) for t in self.__slots["data"]["petTeams"]]
    
    @property
    def active_pets(self) -> List[Pet]:
        if "petSlots" in self.__slots["data"]:
            return [Pet(p) for p in self.__slots["data"]["petSlots"]]


class GameState(ReprMixin):
    def __init__(self, ws_manager: WSManager, current_user_name: str):
        self.__state: Dict = None
        self.__current_user_name: str = current_user_name
        self.__ws = ws_manager
        self.__ws.add_inbound_handler(self._state_monitor)
        self.is_ready: asyncio.Event = asyncio.Event()


    def __upd_raw_state(self, json_patches: List[Dict]):
        apply_patch(self.__state, json_patches, in_place=True)


    def __init_raw_state(self, fullstate: Dict):
        self.__state = fullstate


    def save_raw_state(self, path: str):
        with open(path, 'w') as f:
            f.write(json.dumps(self.__state, indent=4))


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

    
    def _state_monitor(self, msg: str):
        if self.__check_msg_is_typed(msg):
            msg = self.__decode_msg(msg)
            if msg["type"] == "Welcome":
                self.__init_raw_state(msg["fullState"])
            if msg["type"] == "RoomFrame":
                if "state" not in msg.keys():
                    return
                else:
                    self.__upd_raw_state(msg["state"]["patches"])
                    if not self.is_ready.is_set() and not self.players is None:
                        self.is_ready.set()
    

    @property
    def currentWeather(self):
        return Weather(self.__state["child"]["data"]["weather"])


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
