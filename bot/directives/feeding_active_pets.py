import asyncio
from typing import Optional, Tuple
import time
from uuid import uuid4

from bot.directives.bot_directive import BotDirective
from game.commands import HarvestCrop, FeedPet
from game.game_types import ItemType, PetSpecies, ToolId, Species, EggId, Shops, Unknown, ObjectType
from game.state import Item



class FeedingActivePets(BotDirective):

    async def __try_harvest_crop(self, spec: Species) -> Optional[str]:
        now_ms = ms = int(time.time() * 1000)
        tiles = [t for t in self.game_state.currentPlayer.garden.gardenTiles if not t.object_in_tile is None]
        plant_tiles = [t for t in tiles if t.object_in_tile.objectType == ObjectType.PLANT]
        if len(plant_tiles) == 0:
            print(f'[/feeding_active_pet] [/harvest] No plant tiles in you garden')
            return
        spec_tile_filter = [t for t in plant_tiles if t.object_in_tile.species==spec]
        if len(spec_tile_filter) == 0:
            print(f'[/feeding_active_pet] [/harvest] No {spec.value} plants in you garden')
            return
        matured_tiles_filter = [t for t in spec_tile_filter if any([s.endTime < now_ms for s in t.object_in_tile.slots])]
        if len(matured_tiles_filter) == 0:
            print(f'[/feeding_active_pet] [/harvest] No matured {spec.value} in you garden')
            return
        matured_tile = matured_tiles_filter[0]
        matured_slot = [s for s in matured_tile.object_in_tile.slots if s.endTime < now_ms][0]
        for i in range(10):
            crop_id = str(uuid4())
            command = HarvestCrop(
                slot=matured_tile.tile_no,
                slotIndex=matured_slot.slotId,
                cropItemId=crop_id
            )
            result = await self.command_provider.execute(command=command)
            if result.ok:
                print(f'[/feeding_active_pet] [/harvest]\t[{i}] Success harvest {spec.value}!')
                return crop_id
                break
            else:
                print(f'[/feeding_active_pet] [/harvest]\t[{i}] Fail harvest {spec.value}: {result.code}')
                await asyncio.sleep(0.2)
        return 

    async def _directive_loop(self):
        while True:
            await asyncio.sleep(10)
            if not self.is_working.is_set():
                break 
            print('[/feeding_active_pet] directive running...')
            active_pets = self.game_state.currentPlayer.active_pets
            hunger_pets_filter = [p for p in active_pets if p.hunger < 100]
            if len(hunger_pets_filter) == 0:
                print(f'[/feeding_active_pet] Dont have hunger pets')
                continue
            pet_diets = self.config.directives.feeding_active_pets.pet_priority_diet
            for pet in hunger_pets_filter:
                pet_diet_filter = [d for d in pet_diets if d.pet==pet.petSpecies]
                if len(pet_diet_filter) == 0:
                    print(f'[/feeding_active_pet] No diet selected for {pet.petSpecies.value}')
                    continue
                pet_diet = pet_diet_filter[0]
                for spec in pet_diet.diet:
                    harvest_result = None
                    inventory_spec_filter = [i for i in self.game_state.currentPlayer.inventory if i.itemUName==spec and i.itemType==ItemType.PRODUCE]
                    if len(inventory_spec_filter) == 0:
                        print(f'[/feeding_active_pet] Dont have {spec.value} for feeding {pet.petSpecies.value}')
                        print(f'[/feeding_active_pet] Try to harvest any {spec.value}...')
                        harvest_result = await self.__try_harvest_crop(spec)
                        if not harvest_result:
                            print(f'[/feeding_active_pet] Fail harvest any {spec.value} :(')
                            continue
                        else:
                            print(f'[/feeding_active_pet] Success harvest {spec.value} :)')
                    item_id = inventory_spec_filter[0].id if harvest_result is None else harvest_result
                    print(f'[/feeding_active_pet] Feeding {pet.petSpecies.value} with {spec.value}...')
                    for i in range(10):
                        command = FeedPet(
                            pet_item_id=pet.id,
                            crop_item_id=item_id
                        )
                        result = await self.command_provider.execute(command=command)
                        if result.ok:
                            print(f'[/feeding_active_pet]\t[{i}] Success feeding {pet.petSpecies.value} with {spec.value}!')
                            break
                        else:
                            print(f'[/feeding_active_pet]\t[{i}] Fail feeding {pet.petSpecies.value} with {spec.value}: {result.code}')
                            await asyncio.sleep(0.2)
                    break


    def ok(self) -> Tuple[bool, Optional[str]]:
        directive_settings = self.config.directives.feeding_active_pets
        for diet in directive_settings.pet_priority_diet:
            if diet.pet == PetSpecies.UNKNOWN:
                return False, "Unknown pet species"
            if any([d==Species.UNKNOWN for d in diet.diet]):
                return False, "Unknown diet"
        return True, ""
