from dataclasses import dataclass
import asyncio
from uuid import uuid4
from abc import ABC, abstractmethod
import json
from typing import Optional, Union, Dict, Tuple

from game.game_types import CommandType



class ACommand(ABC):
    def __init__(self, type: CommandType, result_baseclass):
        self.requestId = str(uuid4())
        self.commandSequence = 0
        self.comand_type: CommandType = type
        self.result: ACommandResult = None
        self._future: asyncio.Future = asyncio.get_running_loop().create_future()
        self.result_baseclass = result_baseclass


    def set_result(self, raw_result: Dict):
        if not raw_result["ok"]:
            self.result = FailResult(**raw_result)
        else:
            self.result = self.result_baseclass(**raw_result)
        self._future.set_result(self.result)

    def set_sequence(self, seq: int):
        self.commandSequence = seq

    @abstractmethod
    def _build_command(self) -> Dict:
        pass


    def build_command(self) -> str:
        command =  {
            "scopePath": [
                "Room",
                "Quinoa"
            ],
            "type": "QuinoaCommand",
            "requestId": self.requestId,
            "commandSequence": self.commandSequence,
            "command": self._build_command()
        }
        return json.dumps(command)


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
