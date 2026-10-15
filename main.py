import asyncio
from typing import Dict, List

from playwright.async_api import async_playwright, WebSocketRoute

from game.state import GameState
from ws_manager import WSManager
from game.commands import CommandProvider, PurchaseShopItem
from game.game_types import Shops, Species, ItemType
from config import Config
from bot import Bot


STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
});
"""

config = Config.loads_from_yaml('./config.yaml')


async def main():

    ws_manager = WSManager()
    command_provider = CommandProvider(ws_manager=ws_manager)
    game_state = GameState(ws_manager=ws_manager, current_user_name=config.auth.user_name)
    bot = Bot(conf=config, game_state=game_state, command_provider=command_provider)

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)

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

        await page.goto("https://magicgarden.gg/r/GKTQ")


        await asyncio.to_thread(input, 'press to start bot...')
        directive_loop_task = asyncio.create_task(bot.run_directive_loop())

        await directive_loop_task
        await browser.close()



asyncio.run(main())
