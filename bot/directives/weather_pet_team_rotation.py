import asyncio

from game.commands import ApplyPetTeam
from game.game_types import Weather
from bot.directives.bot_directive import BotDirective



class WeatherPetRotationDirective(BotDirective):
    def __init__(self, conf, state, command):
        super().__init__(conf, state, command)
        self.weather_teams = {
            Weather.CLEAR: self.config.directives.weather_pet_teams_rotation.weather_teams.default_team,
            Weather.FROST: self.config.directives.weather_pet_teams_rotation.weather_teams.snow,
            Weather.RAIN: self.config.directives.weather_pet_teams_rotation.weather_teams.rain,
            Weather.THUNDERSTORM: self.config.directives.weather_pet_teams_rotation.weather_teams.thunder
        }

    async def _directive_loop(self):
        while True:
            if not self.is_working.is_set():
                break 
            print('[/weather_pet_rotation] directive running...')
            await asyncio.sleep(10)
            current_weather = self.game_state.currentWeather
            if current_weather == Weather.UNKNOWN:
                print('[/weather_pet_rotation] [!] Unknown weather now')
                continue
            weather_team = self.weather_teams[current_weather]
            if weather_team is None:
                print(f'[/weather_pet_rotation] No selected teams to {current_weather.value}')
                continue
            weather_team = [t for t in self.game_state.currentPlayer.petTeams if t.name==weather_team.team_name][0]
            print(f'[/weather_pet_rotation] Now is {current_weather.value}. Try to apply {weather_team.name} team..')
            for i in range(10):
                command = ApplyPetTeam(teamId=weather_team.id)
                result = await self.command_provider.execute(command=command)
                if result.ok:
                    print(f'[/weather_pet_rotation]\t[{i}] Success')
                    break
                else:
                    print(f'[/weather_pet_rotation]\t[{i}] Fail: {result.code}')
            

    def ok(self):
        invalid_flg = False
        msg = None
        not_found_teams = []
        for weather, team in self.weather_teams.items():
            if team is None:
                continue
            weather_team_filter = [t for t in self.game_state.currentPlayer.petTeams if t.name==team.team_name]
            if len(weather_team_filter) == 0:
                not_found_teams.append(team.team_name)
                invalid_flg = True
        if invalid_flg:
            msg = f'Not found team(s): {not_found_teams}'
        return not invalid_flg, msg
