import asyncio
from typing import Dict, List

from playwright.async_api import async_playwright, WebSocketRoute, BrowserContext

from game.state import GameState
from ws_manager import WSManager
from game.commands import CommandProvider
from config import Config
from bot.bot import Bot


STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
});
"""

config = Config.loads_from_yaml('./config.yaml')


async def state_saver(context: BrowserContext):
    while True:
        await context.storage_state(path="./data/auth_state.json")
        await asyncio.sleep(60)

async def main():

    ws_manager = WSManager()
    command_provider = CommandProvider(ws_manager=ws_manager)
    game_state = GameState(ws_manager=ws_manager, current_user_name=config.auth.user_name)
    bot = Bot(conf=config.bot, game_state=game_state, command_provider=command_provider)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=config.bot.headless_mode)

        context = await browser.new_context(
            storage_state="./data/auth_state.json",
            viewport={"width": 900, "height": 600},
            locale="en-US",
        )
        await context.add_init_script(script=STEALTH_SCRIPT)

        page = await context.new_page()
        await page.route_web_socket(
            "**",
            lambda ws: ws_manager.set_websocket(ws),
        )

        await page.goto(f"{config.auth.base_game_path}{config.auth.room_id}")


        await bot.run()

        await asyncio.to_thread(input, "")
        game_state.save_raw_state('./data/gss_test.json')

        bot.stop()

        # await state_saver(context=context)
        
        await browser.close()



asyncio.run(main())
