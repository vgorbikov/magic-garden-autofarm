import asyncio
from playwright.async_api import async_playwright, WebSocketRoute, Playwright

STEALTH_SCRIPT = """
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined,
});
"""

async def run(playwright: Playwright):
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    context = await browser.new_context(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport={'width': 1512, 'height': 982},
        locale='en-US'
    )
    await context.add_init_script(STEALTH_SCRIPT)
    page = await context.new_page()
    await page.goto("https://magicgarden.gg/r/GKTQ")

    await asyncio.to_thread(input, "Нажмите Enter для сохранения состояния... ")
    
    # Сохраняем ВСЕ состояние: куки (включая сессионные) + localStorage
    await context.storage_state(path="./data/auth_state.json")

    await browser.close()

async def main():
    async with async_playwright() as playwright:
        await run(playwright)
asyncio.run(main())