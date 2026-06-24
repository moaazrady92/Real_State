# scrapers/nawy_test3.py
import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
        )
        await page.goto(
            "https://www.nawy.com/search?type=apartment&purpose=sale",
            wait_until="networkidle",
            timeout=30000
        )
        await page.wait_for_timeout(4000)

        # Get first 3 card HTMLs
        cards = await page.query_selector_all("[class*='card']")
        print(f"Cards found: {len(cards)}")

        for i, card in enumerate(cards[:3]):
            html = await card.inner_html()
            print(f"\n--- CARD {i+1} ---")
            print(html[:2000])

        input("\nPress Enter to close...")
        await browser.close()

asyncio.run(inspect())