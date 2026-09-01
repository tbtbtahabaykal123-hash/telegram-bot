import os
import time
import requests
from flask import Flask
from threading import Thread

# Flask Web Server
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Aktif!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# TELEGRAM BOT VE KANAL AYARLARI
BOT_TOKEN = "YENİ_TOKENİ_BURAYA_YAPIŞTIR" # BotFather'ın verdiği yeni token
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 47

def generate_status_text():
    now = time.gmtime(time.time() + 3 * 3600)
    time_str = time.strftime("%d.%m.%Y %H:%M:%S", now)
    
    return f"""KABUS RENT

┌──────────────────────┐
  🟢 Müsait Hesaplar
└──────────────────────┘

[Hesap 1](https://t.me/kabusxkira/3)
[Hesap 8](https://t.me/kabusxkira/40)

┌──────────────────────┐
  🔴 Meşgul Hesaplar
└──────────────────────┘

[Hesap 2](https://t.me/kabusxkira/10) - Ekstra Gece Paketi Devrede
[Hesap 3](https://t.me/kabusxkira/12) - Gece Paketi Devrede
[Hesap 4](https://t.me/kabusxkira/14) - Ekstra Gece Paketi Devrede
[Hesap 5](https://t.me/kabusxkira/19) - Gece Paketi Devrede
[Hesap 6](https://t.me/kabusxkira/22) - Ekstra Gece Paketi Devrede
[Hesap 7](https://t.me/kabusxkira/34) - Ekstra Gece Paketi Devrede

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
        res = requests.post(url, json=payload, timeout=10)
        print("Güncelleme yanıtı:", res.json())
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
    
    while True:
        update_message()
        time.sleep(60)
