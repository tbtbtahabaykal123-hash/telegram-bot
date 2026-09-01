import os
import time
import requests
from flask import Flask
from threading import Thread

# Flask Web Server (Render kapanmasın diye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Aktif!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# TELEGRAM AYARLARI
BOT_TOKEN = "8897902804:AAEdFWs9V41gcUipSrE0_n6LPpAz5VOh5D0"
CHANNEL_ID = "@btkabus"
MESSAGE_ID = 1234

def generate_status_text():
    # Türkiye saatini manuel hesaplama (Kütüphane hatası olmasın diye)
    now = time.gmtime(time.time() + 3 * 3600)
    time_str = time.strftime("%d.%m.%Y %H:%M:%S", now)
    
    return f"""KABUS RENT

┌──────────────────────┐
  🟢 Müsait Hesaplar
└──────────────────────┘

[Hesap 1](https://t.me/kabusxkira/33)
[Hesap 8](https://t.me/kabusxkira/40)

┌──────────────────────┐
  🔴 Meşgul Hesaplar
└──────────────────────┘

[Hesap 2](https://t.me/kabusxkira/34) - Ekstra Gece Paketi Devrede
[Hesap 3](https://t.me/kabusxkira/35) - Gece Paketi Devrede
[Hesap 4](https://t.me/kabusxkira/36) - Ekstra Gece Paketi Devrede
[Hesap 5](https://t.me/kabusxkira/37) - Gece Paketi Devrede
[Hesap 6](https://t.me/kabusxkira/38) - Ekstra Gece Paketi Devrede
[Hesap 7](https://t.me/kabusxkira/39) - Ekstra Gece Paketi Devrede

⏱️ Son Güncelleme: {time_str}

Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.

Hemen kiralamak için;
✅ @btkabus"""

def update_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": CHANNEL_ID,
        "message_id": MESSAGE_ID,
        "text": generate_status_text(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    # Flask başlat
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    # Mesaj güncelleme döngüsü
    while True:
        update_message()
        time.sleep(60)
