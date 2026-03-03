import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    async with async_playwright() as p:
        print("Sistem başlatılıyor, Koray. Hazır mısın?")
        
        try:
            # ÖNEMLİ: Kendi indirdiğimiz tarayıcıyı değil, 
            # Render sisteminde varsayılan olarak bulunanı arar.
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox", 
                    "--disable-setuid-sandbox", 
                    "--disable-dev-shm-usage"
                ]
            )
            
            page = await browser.new_page()
            print("Siteye giriş yapılıyor...")
            await page.goto("https://www.google.com")
            
            title = await page.title()
            print(f"BAŞARILI! Sayfa Başlığı: {title}")
            print("Bot şu an bulutta aktif.")

            while True:
                await asyncio.sleep(3600)
                
        except Exception as e:
            print(f"Hata detayı: {e}")

if __name__ == "__main__":
    asyncio.run(run_bot())