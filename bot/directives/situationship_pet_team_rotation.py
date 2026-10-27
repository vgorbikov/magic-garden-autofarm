import asyncio
from typing import Optional, Tuple
import time
from uuid import uuid4

from bot.directives.bot_directive import BotDirective
from bot.bot import Bot
from game.game_types import ItemType, PetSpecies, ToolId, Species, EggId, Shops, Unknown, ObjectType
from game.state import Item



class SituationshotPetRotation(BotDirective):
    def __init__(self, bot: Bot):
        super().__init__(bot)
        self.stopped = asyncio.Event()
        self.before_pet_set = []

    def __before_pet_set_save(self):
        self.before_pet_set = [p for p in self.game_state.currentPlayer.active_pets]

    def __apply_before_pet_set(self):
        pass

    async def on_harvest(self):
        team_conf = self.config.directives.situationsip_pet_team_rotation.situationship_teams.on_harvest
        self.__before_pet_set_save()
        if team_conf is None:
            return
        team = [t for t in self.game_state.currentPlayer.petTeams if t.name == team_conf.team_name][0]
        apply_result = await self.bot.try_apply_pet_team(team_id=team.id)
        if apply_result:
            print(f'[/situationship_pet_rotation] Success apply {team.name} on sharvest')
        else:
            print(f'[/situationship_pet_rotation] Failed apply {team.name} on harvest')
        await asyncio.sleep(1)

    async def on_pet_sell(self):
        team_conf = self.config.directives.situationsip_pet_team_rotation.situationship_teams.on_sell_pets
        self.__before_pet_set_save()
        if team_conf is None:
            return
        team = [t for t in self.game_state.currentPlayer.petTeams if t.name == team_conf.team_name][0]
        apply_result = await self.bot.try_apply_pet_team(team_id=team.id)
        if apply_result:
            print(f'[/situationship_pet_rotation] Success apply {team.name} on sell pets')
        else:
            print(f'[/situationship_pet_rotation] Failed apply {team.name} on sell pets')
        await asyncio.sleep(1)

    async def on_pet_hutch(self):
        team_conf = self.config.directives.situationsip_pet_team_rotation.situationship_teams.on_pets_hutch
        self.__before_pet_set_save()
        if team_conf is None:
            return
        team = [t for t in self.game_state.currentPlayer.petTeams if t.name == team_conf.team_name][0]
        apply_result = await self.bot.try_apply_pet_team(team_id=team.id)
        if apply_result:
            print(f'[/situationship_pet_rotation] Success apply {team.name} on hutch pets')
        else:
            print(f'[/situationship_pet_rotation] Failed apply {team.name} on hutch pets')
        await asyncio.sleep(1)

    async def _directive_loop(self):
        self.bot.event_callouts.on_harvest.before.append(self.on_harvest)
        self.bot.event_callouts.on_pet_sell.before.append(self.on_pet_sell)
        self.bot.event_callouts.on_hutch.before.append(self.on_pet_hutch)
        await self.stopped()

    def off(self):
        self.is_working.clear()
        self.stopped.set()

    def ok(self) -> Tuple[bool, Optional[str]]:
        teams = self.config.directives.situationsip_pet_team_rotation.situationship_teams
        user_team_names = [t.name for t in self.game_state.currentPlayer.petTeams]
        for team_name in [teams.on_harvest.team_name, teams.on_pets_hutch.team_name, teams.on_sell_crops.team_name, teams.on_sell_pets.team_name]:
            if team_name not in user_team_names:
                return False, f"Unknown team: {team_name}"
        return True, ""
