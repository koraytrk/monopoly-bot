import os
import time
import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

# .env dosyasındaki bilgileri yükle
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def telegram_mesaj_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mesaj}
    try:
        requests.post(url, data=payload)
        print("✅ Telegram mesajı gönderildi.")
    except Exception as e:
        print(f"❌ Telegram hatası: {e}")

def monopoly_kontrol_et():
    with sync_playwright() as p:
        # headless=False: Tarayıcı penceresini görünür yapar
        # slow_mo=500: İşlemleri izleyebilmen için biraz yavaşlatır
        browser = p.chromium.launch(headless=False) 
        
        context = browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print(f"[{time.strftime('%H:%M:%S')}] Tarayıcı açıldı, sayfaya gidiliyor...")
            
            # Sayfaya git ve tamamen yüklenmesini (networkidle) bekle
            page.goto("https://tracksino.com/monopoly-big-baller", wait_until="networkidle", timeout=60000)
            
            # Sayfa açıldıktan sonra verilerin gelmesi için 5 saniye bekle
            print("⏳ Veriler yükleniyor, lütfen bekle...")
            page.wait_for_timeout(5000)
            
            # '5 Rolls' yazısını içeren elementi bul
            element = page.get_by_text("5 Rolls").first
            
            if element:
                veri = element.inner_text()
                print(f"🔍 Okunan Veri: {veri}")
                
                # 'hour' geçiyorsa veya 120 dakikayı geçmişse
                if "hour" in veri.lower() or "120" in veri:
                    telegram_mesaj_gonder(f"🚨 KORAY ALARM!\nMonopoly 5 Rolls gelmeyeli {veri} olmuş.\nYaklaşıyor olabilir!")
                else:
                    print("ℹ️ Kritik süre henüz dolmadı.")
            else:
                print("⚠️ Ekranda '5 Rolls' yazısı bulunamadı.")

        except Exception as e:
            print(f"❌ Hata oluştu: {e}")
        finally:
            # İşlem bitince tarayıcıyı kapat (Ekranda kalmasını istersen bu satırı silebilirsin)
            browser.close()

# Botu Başlat
if __name__ == "__main__":
    print("--- Bot Başlatıldı, Koray! (Görünür Mod) ---")
    while True:
        monopoly_kontrol_et()
        print("😴 1 dakika bekleniyor...")
        time.sleep(60)
        