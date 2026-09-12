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

MESSAGE_ID = None

def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 2](https://t.me/kabusxkira/10)",
        "[Hesap 4](https://t.me/kabusxkira/14)",
        "[Hesap 5](https://t.me/kabusxkira/19)",
        "[Hesap 6](https://t.me/kabusxkira/22)",
        "[Hesap 7](https://t.me/kabusxkira/34)",
        "[Hesap 8](https://t.me/kabusxkira/40)",
        "[Hesap 9](https://t.me/kabusxkira/49)"
    ]

    mesgul_hesaplar = [
        "[Hesap 3](https://t.me/kabusxkira/12) - Gece Paketi Devrede"
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

def send_fresh_message():
    global MESSAGE_ID
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": get_message_text(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    try:
        res = requests.post(url, json=payload, timeout=10).json()
        if res.get("ok"):
            MESSAGE_ID = res["result"]["message_id"]
            print(f"YENİ MESAJ ATILDI. MESSAGE_ID: {MESSAGE_ID}")
            return res
    except Exception as e:
        print("Mesaj atılamadı:", e)
    return None

def update_telegram_message():
    global MESSAGE_ID

    if MESSAGE_ID is None:
        return send_fresh_message()

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
            print("Düzenleme başarısız, sıfırdan mesaj atılıyor...")
            return send_fresh_message()
        return res
    except Exception as e:
        return {"error": str(e)}

def auto_loop():
    time.sleep(3)
    # İlk açılışta direk yeni mesaj at
    send_fresh_message()
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
