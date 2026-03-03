import os
import asyncio
from playwright.async_api import async_playwright

async def run_bot():
    # Render'ın tarayıcıyı kurduğu gizli yolu koda gösteriyoruz
    # Hata mesajında çıkan 'chromium-1105' yolunu baz aldık
    chrome_path = "/opt/render/.cache/ms-playwright/chromium-1105/chrome-linux/chrome"

    async with async_playwright() as p:
        print("Sistem başlatılıyor, Koray. Tarayıcı kontrol ediliyor...")
        
        try:
            # Tarayıcıyı Render'ın izin verdiği özel ayarlarla açıyoruz
            browser = await p.chromium.launch(
                headless=True,
                executable_path=chrome_path,
                args=[
                    "--no-sandbox", 
                    "--disable-setuid-sandbox", 
                    "--disable-dev-shm-usage",
                    "--disable-gpu"
                ]
            )
            
            context = await browser.new_context()
            page = await context.new_page()
            
            # TEST: Google'a gidip bağlantıyı kontrol edelim
            print("Siteye giriş yapılıyor...")
            await page.goto("https://www.google.com", timeout=60000)
            
            title = await page.title()
            print(f"Bağlantı Başarılı! Sayfa Başlığı: {title}")
            print("Bot şu an bulutta aktif olarak çalışıyor.")

            # --- KENDİ BOT MANTIKLARINI (TELEGRAM VS.) BURAYA EKLEYEBİLİRSİN ---
            
            # Botun hemen kapanmaması için bekletiyoruz
            await asyncio.sleep(300) 
            
            await browser.close()
            
        except Exception as e:
            print(f"Bir hata oluştu Koray: {e}")
            print("Eğer 'executable doesn't exist' diyorsa Render panelinden 'Clear Build Cache' yapmalısın.")

if __name__ == "__main__":
    # Render'daki asenkron yapıyı başlatır
    asyncio.run(run_bot())
    