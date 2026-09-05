import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = "8897902804:AAGRP_5WH87wngvCczarPM1w5AF7u-uaAUc"
CHANNEL_ID = "@kabusxkira"

# Doğru Mesaj ID
MESSAGE_ID = 52

# Hedef Zaman (Hesap 5 Kiralama Bitişi)
HESAP5_TARGET_TS = 1788814847

def get_countdown(target_ts):
    now_utc = time.time()
    diff = int(target_ts - now_utc)
    
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
    # Türkiye Saati (UTC+3)
    now_ts = time.time() + (3 * 3600)
    now = time.gmtime(now_ts)
    current_hour = now.tm_hour
    time_str = time.strftime('%d.%m.%Y %H:%M:%S', now)

    # Otomatik Zaman Kontrolü (00:00 - 10:00 / 13:00 Meşgul)
    gece_mesgul = current_hour < 10
    ekstra_mesgul = current_hour < 13

    musait_hesaplar = []
    mesgul_hesaplar = []

    # Standart Gece Paketleri (1, 6, 7, 8, 9)
    gece_hesaplari = [
        ("[Hesap 1](https://t.me/kabusxkira/3)", "Gece Paketi Devrede"),
        ("[Hesap 6](https://t.me/kabusxkira/22)", "Gece Paketi Devrede"),
        ("[Hesap 7](https://t.me/kabusxkira/34)", "Gece Paketi Devrede"),
        ("[Hesap 8](https://t.me/kabusxkira/40)", "Gece Paketi Devrede"),
        ("[Hesap 9](https://t.me/kabusxkira/49)", "Gece Paketi Devrede")
    ]

    # Ekstra Gece Paketleri (2, 3, 4)
    ekstra_hesaplar = [
        ("[Hesap 2](https://t.me/kabusxkira/10)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 3](https://t.me/kabusxkira/12)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 4](https://t.me/kabusxkira/14)", "Ekstra Gece Paketi Devrede")
    ]

    # Standart Gece Paketlerini Kontrol Et
    for link, label in gece_hesaplari:
        if gece_mesgul:
            mesgul_hesaplar.append(f"{link} - {label}")
        else:
            musait_hesaplar.append(link)

    # Ekstra Gece Paketlerini Kontrol Et
    for link, label in ekstra_hesaplar:
        if ekstra_mesgul:
            mesgul_hesaplar.append(f"{link} - {label}")
        else:
            musait_hesaplar.append(link)

    # Sayaçlı Hesap (Hesap 5)
    hesap5_timer = get_countdown(HESAP5_TARGET_TS)
    if hesap5_timer:
        mesgul_hesaplar.append(f"[Hesap 5](https://t.me/kabusxkira/19) - {hesap5_timer}")
    else:
        musait_hesaplar.append("[Hesap 5](https://t.me/kabusxkira/19)")

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
        res = requests.post(url, json=payload, timeout=10).json()
        return res
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
