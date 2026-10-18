import asyncio

from game.state import GameState
from game.commands import CommandProvider
from bot.directives import ShopItemsDirecrtive, WeatherPetRotationDirective
from config import BotConf



class Bot():
    def __init__(self, conf: BotConf, game_state: GameState, command_provider: CommandProvider):
        self.game_state: GameState = game_state
        self.command_provider: CommandProvider = command_provider
        self.config: BotConf = conf
        self.is_running: asyncio.Event = asyncio.Event()
        self.shop_item_directive = ShopItemsDirecrtive(
            conf=self.config,
            state=self.game_state,
            command=self.command_provider
        )
        self.weather_pet_rotation_directive = WeatherPetRotationDirective(
            conf=self.config,
            state=self.game_state,
            command=self.command_provider
        )
        

    async def run(self):
        await self.game_state.is_ready.wait()
        await self.command_provider.is_ready.wait()
        self.is_running.set()
        print('<i> bot is running')

        if self.config.directives.shop_items.status:
            ok, msg = self.shop_item_directive.ok()
            if ok:
                self.shop_item_directive.on()
                print('<i> shop items directive is on')
            else:
                print(f'<E> Fail to run shop item directive: {msg}')
        if self.config.directives.weather_pet_teams_rotation:
            ok, msg = self.weather_pet_rotation_directive.ok()
            if ok:
                self.weather_pet_rotation_directive.on()
                print('<i> weather pet teams rotation directive is on')
            else:
                print(f'<E> Fail to run weather pet teams rotation directive: {msg}')


    def stop(self):
        if self.config.directives.shop_items.status:
            self.shop_item_directive.off()
        if self.config.directives.weather_pet_teams_rotation:
            self.weather_pet_rotation_directive.off()
