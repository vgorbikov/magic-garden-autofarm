import asyncio
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from game.state import GameState
from game.commands import CommandProvider
from config import Config



class BotDirective(ABC):

    def __init__(self, conf: Config, state: GameState, command: CommandProvider):
        self.game_state: GameState = state
        self.command_provider: CommandProvider = command
        self.config: Config = conf
        self.is_working: asyncio.Event = asyncio.Event()
        self.loop_task: asyncio.Task = None

    @abstractmethod
    async def _directive_loop(self):
        pass

    @abstractmethod
    def ok(self) -> Tuple[bool, Optional[str]]:
        pass 

    def on(self):
        self.is_working.set()
        self.loop_task = asyncio.create_task(self._directive_loop())


    def off(self):
        self.is_working.clear()
