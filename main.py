import asyncio
from typing import Dict, List

from playwright.async_api import async_playwright, WebSocketRoute
import json

from ws_manager import WSManager
from game import Game, Species
from config import Config


STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
});
"""

config = Config.loads_from_yaml('./config.yaml')


async def main():

    ws_manager = WSManager()
    game = Game(config=config)
    ws_manager.add_inbound_handler(game.handle_server_msg)
    game.set_ws_manager(ws_manager)

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


        await game.loop_print_state()

        # await asyncio.to_thread(input, 'hold to buy...')
        # game.buy_seed(Species.CARROT, 1)

        await asyncio.to_thread(input, 'hold...')
        game.state.save_raw_state("./data/game_saved_state.json")

        # await browser.close()



asyncio.run(main())
