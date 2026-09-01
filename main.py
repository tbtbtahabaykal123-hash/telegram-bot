import os
import time
import requests
import threading
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "OK"

BOT_TOKEN = "8897902804:AAEdFWs9V41gcUipSrE0_n6LPpAz5VOh5D0"
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 47

def update_loop():
    time.sleep(3)
    while True:
        try:
            now_ts = time.time() + (3 * 3600)
            now = time.gmtime(now_ts)
            ms = int((now_ts % 1) * 10)
            time_str = f"{time.strftime('%d.%m.%Y %H:%M:%S', now)}.{ms}"
            
            text = f"""KABUS RENT

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

            url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
            payload = {
                "chat_id": CHANNEL_ID,
                "message_id": MESSAGE_ID,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            }
            res = requests.post(url, json=payload, timeout=10)
            print("TELEGRAM CEVAP:", res.json())
        except Exception as e:
            print("HATA:", e)
            
        time.sleep(60)

# KOD DOSYASI YÜKLENDİĞİ AN DÖNGÜYÜ BAŞLAT (Web sunucusundan bağımsız)
threading.Thread(target=update_loop, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
