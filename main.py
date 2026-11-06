import os
import time
import requests
from datetime import datetime, timezone, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

# Token'ı doğrudan açık yazmıyoruz, Render ortam değişkeninden gizlice alıyor
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@kabusxkira"

# Sabit Mesaj ID
MESSAGE_ID = 58

def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 2](https://t.me/kabusxkira/10)",
        "[Hesap 3](https://t.me/kabusxkira/12)",
        "[Hesap 4](https://t.me/kabusxkira/14)",
        "[Hesap 5](https://t.me/kabusxkira/19)",
        "[Hesap 6](https://t.me/kabusxkira/22)",
        "[Hesap 7](https://t.me/kabusxkira/34)",
        "[Hesap 8](https://t.me/kabusxkira/40)",
        "[Hesap 9](https://t.me/kabusxkira/49)"
    ]
    
    mesgul_hesaplar = []

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
    if not BOT_TOKEN:
        print("HATA: BOT_TOKEN bulunamadı!")
        return {"error": "Token yok"}

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
