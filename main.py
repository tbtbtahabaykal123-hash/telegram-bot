import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = "8897902804:AAGRP_5WH87wngvCczarPM1w5AF7u-uaAUc"
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 47

# Hesap 2 Bitiş Zamanı: TSİ 02.09.2026 Saat 22:40:00 (UTC 19:40:00)
HESAP2_TARGET_TS = 1788378000

def get_hesap2_countdown():
    now_utc = time.time()
    diff = int(HESAP2_TARGET_TS - now_utc)
    
    if diff <= 0:
        return None
    
    days = diff // 86400
    rem = diff % 86400
    hours = rem // 3600
    rem %= 3600
    minutes = rem // 60
    seconds = rem % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} G")
    if hours > 0 or days > 0:
        parts.append(f"{hours} Saat")
    if minutes > 0 or hours > 0 or days > 0:
        parts.append(f"{minutes} Dk")
    parts.append(f"{seconds} Sn")
    
    return " ".join(parts) + " Var"

def update_telegram_message():
    # Türkiye Saati Gösterimi (UTC+3)
    now_ts = time.time() + (3 * 3600)
    now = time.gmtime(now_ts)
    time_str = time.strftime('%d.%m.%Y %H:%M:%S', now)

    # 🟢 Müsait Hesaplar (1 ve 7)
    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 7](https://t.me/kabusxkira/34)"
    ]
    
    # 🔴 Meşgul Listesi
    mesgul_hesaplar = []

    # 1. Hesap 2 Kontrolü (Geri Sayım)
    hesap2_remaining = get_hesap2_countdown()
    if hesap2_remaining:
        mesgul_hesaplar.append(f"[Hesap 2](https://t.me/kabusxkira/10) - {hesap2_remaining}")
    else:
        musait_hesaplar.append("[Hesap 2](https://t.me/kabusxkira/10)")

    # 2. Gece Paketi Hesapları (3, 4, 5, 6)
    gece_hesaplari = [
        "[Hesap 3](https://t.me/kabusxkira/12) - Gece Paketi Devrede",
        "[Hesap 4](https://t.me/kabusxkira/14) - Gece Paketi Devrede",
        "[Hesap 5](https://t.me/kabusxkira/19) - Gece Paketi Devrede",
        "[Hesap 6](https://t.me/kabusxkira/22) - Gece Paketi Devrede"
    ]
    mesgul_hesaplar.extend(gece_hesaplari)

    # 3. Ekstra Gece Paketi Hesapları (8)
    mesgul_hesaplar.append("[Hesap 8](https://t.me/kabusxkira/40) - Ekstra Gece Paketi Devrede")

    # Formatlama
    musait_text = "\n".join(musait_hesaplar) if musait_hesaplar else "Yok"
    mesgul_text = "\n".join(mesgul_hesaplar) if mesgul_hesaplar else "Yok"

    text = f"""KABUS RENT

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

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": CHANNEL_ID,
        "message_id": MESSAGE_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        return res.json()
    except Exception as e:
        return {"error": str(e)}

def auto_loop():
    time.sleep(5)
    while True:
        status = update_telegram_message()
        print("OTOMATIK DÖNGÜ SONUCU:", status)
        time.sleep(60)

Thread(target=auto_loop, daemon=True).start()

@app.route('/')
def home():
    status = update_telegram_message()
    return f"Guncelleme Tetiklendi: {status}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
