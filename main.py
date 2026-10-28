import os
import time
import requests
from datetime import datetime, timezone, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

# Güncel Bot Tokenı
BOT_TOKEN = "8897902804:AAFwTzAtr1qx6Umzkkig4Jz6GvsdIwVjORQ"
CHANNEL_ID = "@kabusxkira"

# Kilitlenen ve sadece düzenlenecek mesajın ID'si
MESSAGE_ID = 58

def get_message_text():
    # Türkiye Saati (UTC+3)
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    # 1'den 9'a kadar hepsi Gece Paketinde (Meşgul)
    musait_hesaplar = []
    
    mesgul_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3) - Gece Paketi Devrede",
        "[Hesap 2](https://t.me/kabusxkira/10) - Gece Paketi Devrede",
        "[Hesap 3](https://t.me/kabusxkira/12) - Gece Paketi Devrede",
        "[Hesap 4](https://t.me/kabusxkira/14) - Gece Paketi Devrede",
        "[Hesap 5](https://t.me/kabusxkira/19) - Gece Paketi Devrede",
        "[Hesap 6](https://t.me/kabusxkira/22) - Gece Paketi Devrede",
        "[Hesap 7](https://t.me/kabusxkira/34) - Gece Paketi Devrede",
        "[Hesap 8](https://t.me/kabusxkira/40) - Gece Paketi Devrede",
        "[Hesap 9](https://t.me/kabusxkira/49) - Gece Paketi Devrede"
    ]

    musait_text = "\n".join(musait_hesaplar) if musait_hesaplar else "Yok"
    mesgul_text = "\n".join(mesgul_hesaplar) if mesgul_hesaplar else "Yok"

    return f"""KABUS RENT

┌──────────────────────┐
  🟢 Müsait Hesaplar
└──────────────────────┘

{musait_text}

┌──────────────────────┐
  🔴 Meşgul Hesaplar
└──────────────────────┘

{mesgul_text}

⏱️ Son Güncelleme: {time_str}

Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.

Hemen kiralamak için;
✅ @btkabus"""

def update_telegram_message():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": CHANNEL_ID,
        "message_id": MESSAGE_ID,
        "text": get_message_text(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        res = requests.post(url, json=payload, timeout=10).json()
        if not res.get("ok"):
            print("Düzenleme başarısız. Hata:", res)
        else:
            print(f"Mesaj {MESSAGE_ID} başarıyla güncellendi.")
        return res
    except Exception as e:
        print("Telegram API hatası:", e)
        return {"error": str(e)}

def auto_loop():
    time.sleep(5)
    update_telegram_message()
    while True:
        time.sleep(60)
        status = update_telegram_message()
        print("OTOMATIK DÖNGÜ SONUCU:", status)

Thread(target=auto_loop, daemon=True).start()

@app.route('/')
def home():
    status = update_telegram_message()
    return f"Guncelleme Tetiklendi: {status}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
