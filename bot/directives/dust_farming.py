import asyncio
from typing import Optional, Tuple
import time
from uuid import uuid4

from bot.directives.bot_directive import BotDirective
from game.commands import HarvestCrop, FeedPet
from game.commands.commands import GrowEgg, HatchEgg, SellPet
from game.game_types import ItemType, PetSpecies, ToolId, Species, EggId, Shops, Unknown, ObjectType
from game.state import Item



class Dustfarming(BotDirective):

    async def __try_grow_egg(self, eggId: EggId, tile: int) -> bool:
        for i in range(10):
            command = GrowEgg(
                slot=tile,
                egg_id=eggId
            )
            result = await self.command_provider.execute(command=command)
            if result.ok:
                print(f'[/dust_farming] [/grow_egg]\t[{i}] Success grow {eggId.value}!')
                return True
            else:
                print(f'[/dust_farming] [/grow_egg]\t[{i}] Fail to grow {eggId.value}: {result.code}')
                await asyncio.sleep(0.2)
        return False
    
    async def __try_hatch_eggs(self, slot: int):
        for i in range(10):
            command = HatchEgg(
                slot=slot
            )
            result = await self.command_provider.execute(command=command)
            if result.ok:
                print(f'[/dust_farming] [/hatch_eggs]\t[{i}] Success hatch!')
                return True
            else:
                print(f'[/dust_farming] [/hatch_eggs]\t[{i}] Fail to hatch: {result.code}')
                await asyncio.sleep(0.2)
        return False
    
    async def __try_sell_pet(self, pet_id: str):
        for i in range(10):
            command = SellPet(
                item_id=pet_id
            )
            result = await self.command_provider.execute(command=command)
            if result.ok:
                print(f'[/dust_farming] [/sell_pets]\t[{i}] Success sell pet!')
                return True
            else:
                print(f'[/dust_farming] [/sell_pets]\t[{i}] Fail to sell pet: {result.code}')
                await asyncio.sleep(0.2)
        return False

    async def _directive_loop(self):
        while True:
            await asyncio.sleep(65)
            if not self.is_working.is_set():
                break 
            print('[/dust_farming] directive running...')
            directive_settings = self.config.directives.dust_farming
            eggs_to_use = directive_settings.eggs_to_use
            now_ms = ms = int(time.time() * 1000)
            ## Hatching matured eggs
            tiles = [t for t in self.game_state.currentPlayer.garden.gardenTiles if not t.object_in_tile is None]
            eggs_tiles = [t for t in tiles if t.object_in_tile.objectType==ObjectType.EGG and t.object_in_tile.eggId in eggs_to_use]
            matured_egg_tiles = [t for t in eggs_tiles if t.object_in_tile.maturedAt<now_ms]
            if len(matured_egg_tiles)==0:
                print('[/dust_farming] No matured eggs in garden')
            else:
                print(f'[/dust_farming] Found {len(matured_egg_tiles)} matured eggs. Try to hatch...')
                hatch_happens = False
                for egg_tile in matured_egg_tiles:
                    hatch_result = await self.__try_hatch_eggs(slot=egg_tile.tile_no)
                    if hatch_result:
                        print(f'[/dust_farming] Sucess hatch {egg_tile.object_in_tile.eggId.value}!')
                        hatch_happens = True
                    else: 
                        print(f'[/dust_farming] Fail hatch {egg_tile.object_in_tile.eggId.value}')
                if hatch_happens:
                    ## Selling hatched pats
                    pets_in_inventory = [p for p in self.game_state.currentPlayer.inventory if p.itemType==ItemType.PET]
                    pets_to_sell = [p for p in pets_in_inventory if p.sourceEggId in eggs_to_use] 
                    print(f'[/dust_farming] Hatch happens. Try to sell {len(pets_to_sell)} pets...')
                    for pet in pets_to_sell:
                        sell_result = await self.__try_sell_pet(pet.id)
                        if sell_result:
                            print(f'[/dust_farming] Successful sell {pet.petSpecies.value}')
                        else:
                           print(f'[/dust_farming] Fail to sell {pet.petSpecies.value}')
            ## Grows new eggs
            free_tiles = [t for t in self.game_state.currentPlayer.garden.gardenTiles if t.object_in_tile == None]
            if len(free_tiles)==0:
                print('[/dust_farming] No free tiles to grow eggs')
            else:
                eggs_in_inventory = [e for e in self.game_state.currentPlayer.inventory if e.itemUName in eggs_to_use]
                if len(eggs_in_inventory)==0:
                    print('[/dust_farming] No selected eggs in inventory')
                else:
                    egg = eggs_in_inventory[0]
                    print(f'[/dust_farming] Found {egg.quantity} {egg.eggId.value}. Try to growing...')
                    available_tiles_count = max(len(free_tiles), egg.quantity)
                    available_free_tiles = free_tiles[0:available_tiles_count]
                    for tile in available_free_tiles:
                        grow_result_ok = await self.__try_grow_egg(egg.eggId, tile=tile.tile_no)
            print('[/dust_farming] End iteration')
        

    def ok(self) -> Tuple[bool, Optional[str]]:
        directive_settings = self.config.directives.dust_farming
        for egg in directive_settings.eggs_to_use:
            if egg == EggId.UNKNOWN:
                return False, "Unknown Egg Id"
        return True, ""