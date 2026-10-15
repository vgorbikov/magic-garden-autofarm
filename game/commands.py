from dataclasses import dataclass
import asyncio
from uuid import uuid4
from abc import ABC, abstractmethod
import json
from typing import Optional, Union, Dict, Tuple

from game.game_types import CommandType, Species, ToolId, EggId, DecorId, ItemType, Shops
from ws_manager import WSManager



class ACommand(ABC):
    def __init__(self, type: CommandType):
        self.requestId = str(uuid4())
        self.commandSequence = 0
        self.comand_type: CommandType = type
        self.result: ACommandResult = None
        self.result_baseclass = ACommandResult


    def set_result(self, raw_result: Dict):
        if not raw_result["ok"]:
            self.result = FailResult(**raw_result)
        else:
            self.result = self.result_baseclass(**raw_result)

    def set_sequence(self, seq: int):
        self.commandSequence = seq

    @abstractmethod
    def build_command(self) -> str:
        pass


@dataclass
class ACommandResult():
    requestId: str 
    ok: bool
    commandType: CommandType
    type: str = 'QuinoaCommand'

    def __post_init__(self):
        if not isinstance(self.commandType, CommandType):
            self.commandType = CommandType(self.commandType)
    

@dataclass
class FailResult(ACommandResult):
    code: str = ''


@dataclass
class PurchaseShopItemResult(ACommandResult):
    itemGains: str = ''
    commandType: CommandType = CommandType.PURCHASE_SHOP_ITEM


class PurchaseShopItem(ACommand):
    def __init__(self, shop: Shops, itemType: ItemType, item: Union[ToolId, EggId, Species], count: int = 1):
        super().__init__(CommandType.PURCHASE_SHOP_ITEM)
        self.shop = shop
        self.item_type = itemType
        self.item = item
        self.count = count
        self.result_baseclass = PurchaseShopItemResult

    def build_command(self):
        item_specs = {
            ToolId: "toolId",
            EggId: "eggId",
            Species: "species"
        }
        command =  {
            "scopePath": [
                "Room",
                "Quinoa"
            ],
            "type": "QuinoaCommand",
            "requestId": self.requestId,
            "commandSequence": self.commandSequence,
            "command": {
                "type": self.comand_type.value,
                "shop": self.shop.value,
                "viewMode": "grid",
                "item": {
                    "itemType": self.item_type.value,
                    item_specs[type(self.item)]: self.item.value
                },
                "quantity": self.count
            }
        }
        return json.dumps(command)


class CommandProvider():
    def __init__(self, ws_manager: WSManager):
        self.ws = ws_manager
        self.active_commands: Dict[str, Tuple[asyncio.Future, ACommand]] = dict()
        self.actual_executed_sequence: int = 0
        self.ws.add_inbound_handler(self._monitor_results)
        self.ws.add_inbound_handler(self._monitor_command_sequence)
        self.is_ready: asyncio.Event = self.ws.is_ready

    def __decode_msg(self, msg: str) -> Dict:
        try:
            msg = json.loads(msg)
        except:
            return dict()
        return msg
    
    def _check_msg_is_typed(self, msg: str) -> bool:
        msg = self.__decode_msg(msg)
        if "type" in msg.keys():
            return True 
        return False
    
    def _monitor_command_sequence(self, msg: str):
        if not self._check_msg_is_typed(msg):
            return
        msg = self.__decode_msg(msg)
        if "executedCommandSequence" in msg.keys():
                actual_seq = msg["executedCommandSequence"]
                if  actual_seq != self.actual_executed_sequence:
                    self.actual_executed_sequence = actual_seq

    def _monitor_results(self, msg: str):
        if not self._check_msg_is_typed(msg):
            return
        msg = self.__decode_msg(msg)
        if msg["type"] == 'QuinoaCommandResult':
            if msg["requestId"] in self.active_commands.keys():
                command_waiters = self.active_commands[msg["requestId"]]
                command_waiters[1].set_result(msg)
                command_waiters[0].set_result(command_waiters[1].result)
                self.active_commands.pop(msg["requestId"])

    async def execute(self, command: ACommand) -> ACommandResult:
        command.set_sequence(self.actual_executed_sequence + 1)
        result = asyncio.get_running_loop().create_future()
        self.active_commands[command.requestId] = (result, command)
        self.ws.send_message_to_server(command.build_command(), "COMMAND PROVIDER")
        real_result = await result
        self.actual_executed_sequence += 1
        return real_result
