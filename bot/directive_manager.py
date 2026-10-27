import asyncio

from bot.directives import ShopItemsDirecrtive, WeatherPetRotationDirective, FeedingActivePets, Dustfarming, SituationshotPetRotation
from bot.bot import Bot



class DirectiveManager():
    def __init__(self, bot: Bot):
        self.bot = bot
        self.is_running: asyncio.Event = asyncio.Event()
        self.shop_item_directive = ShopItemsDirecrtive(bot=bot)
        self.weather_pet_rotation_directive = WeatherPetRotationDirective(bot=bot)
        self.feeding_active_pets_directive = FeedingActivePets(bot=bot)
        self.dust_framing = Dustfarming(bot=bot)
        self.situationship_pet_rotation = SituationshotPetRotation(bot=bot)

    async def run(self):
        await self.bot.game_state.is_ready.wait()
        await self.bot.command_provider.is_ready.wait()
        self.is_running.set()
        print('<i> bot is running')

        if self.bot.config.directives.shop_items.status:
            ok, msg = self.shop_item_directive.ok()
            if ok:
                self.shop_item_directive.on()
                print('<i> shop items directive is on')
            else:
                print(f'<E> Fail to run shop item directive: {msg}')
        if self.bot.config.directives.weather_pet_teams_rotation.status:
            ok, msg = self.weather_pet_rotation_directive.ok()
            if ok:
                self.weather_pet_rotation_directive.on()
                print('<i> weather pet teams rotation directive is on')
            else:
                print(f'<E> Fail to run weather pet teams rotation directive: {msg}')
        if self.bot.config.directives.feeding_active_pets.status:
            ok, msg = self.feeding_active_pets_directive.ok()
            if ok:
                self.feeding_active_pets_directive.on()
                print('<i> feeding active pets directive is on')
            else:
                print(f'<E> Fail to run feeding active pets directive: {msg}')
        if self.bot.config.directives.dust_farming.status:
            ok, msg = self.dust_framing.ok()
            if ok:
                self.dust_framing.on()
                print('<i> dust farming directive is on')
            else:
                print(f'<E> Fail to run dust farming directive: {msg}')
        if self.bot.config.directives.situationsip_pet_team_rotation.status:
            ok, msg = self.dust_framing.ok()
            if ok:
                self.situationship_pet_rotation.on()
                print('<i> Situationship pet teams rotation directive is on')
            else:
                print(f'<E> Fail to run situationship pet teams rotation directive: {msg}')


    def stop(self):
        if self.bot.config.directives.shop_items.status:
            self.shop_item_directive.off()
        if self.bot.config.directives.weather_pet_teams_rotation.status:
            self.weather_pet_rotation_directive.off()
        if self.bot.config.directives.feeding_active_pets.status:
            self.feeding_active_pets_directive.off()
        if self.bot.config.directives.dust_farming.status:
            self.dust_framing.off()
        if self.bot.config.directives.situationsip_pet_team_rotation.status:
            self.situationship_pet_rotation.off()
