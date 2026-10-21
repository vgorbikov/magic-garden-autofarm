import asyncio
import json
from typing import Optional, Union, Dict, Tuple

from ws_manager import WSManager
from game.commands.base import ACommand, ACommandResult, FailResult



class CommandProvider():
    def __init__(self, ws_manager: WSManager):
        self.ws = ws_manager
        self.active_commands: Dict[str,  ACommand] = dict()
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
                command = self.active_commands[msg["requestId"]]
                command.set_result(msg)
                self.active_commands.pop(msg["requestId"])

    async def execute(self, command: ACommand) -> ACommandResult:
        command.set_sequence(self.actual_executed_sequence + 1)
        self.actual_executed_sequence += 1
        self.active_commands[command.requestId] = command
        self.ws.send_message_to_server(command.build_command(), "COMMAND PROVIDER")
        try:
            result = await asyncio.wait_for(command._future, timeout=5)
        except:
            result = FailResult(
                requestId=command.requestId,
                ok=False,
                commandType=command.comand_type,
                type="QuinoaCommand",
                code="Future timeout"
            )
        return result
