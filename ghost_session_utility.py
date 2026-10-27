import asyncio
from typing import Dict, List

from playwright.async_api import async_playwright

from config import Config



STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
});
"""

config = Config.loads_from_yaml('./config.yaml')


class GhostSession():
    def __init__(self):
        self.stop_flg: asyncio.Event = asyncio.Event()
        self.__browser = None
        self.__session_task: asyncio.Task = None

    async def __session(self):
        async with async_playwright() as playwright:
            self.__browser = await playwright.chromium.launch(
                headless=False, 
                args=[
                    "--enable-gpu",
                    "--ignore-gpu-blocklist",
                ]
            )

            context = await self.__browser.new_context(
                viewport={"width": 900, "height": 600},
                locale="en-US",
            )
            await context.add_init_script(script=STEALTH_SCRIPT)

            page = await context.new_page()

            await page.goto(f"{config.auth.base_game_path}{config.auth.room_id}")
            print('ghost joined')

            await self.stop_flg.wait()
            print('ghost disconnected')
            
            await self.__browser.close()

    def run_session(self):
        self.__session_task = asyncio.create_task(self.__session())

    async def stop_session(self):
        self.stop_flg.set()
        await self.__session_task


async def run_ghost_sessions(count: int):
    sessions: List[GhostSession] = []
    for i in range(count):
        session = GhostSession()
        sessions.append(session)
        session.run_session()
    await asyncio.to_thread(input, "press to stop")
    for session in sessions:
        await session.stop_session()

asyncio.run(run_ghost_sessions(5))
