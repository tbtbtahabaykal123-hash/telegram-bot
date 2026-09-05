import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = "8897902804:AAGRP_5WH87wngvCczarPM1w5AF7u-uaAUc"
CHANNEL_ID = "@kabusxkira"

MESSAGE_ID = None

# Hedef Zamanlar
HESAP5_TARGET_TS = 1788814847
HESAP6_TARGET_TS = 1788621372

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
    global MESSAGE_ID
    
    now_ts = time.time() + (3 * 3600)
    now = time.gmtime(now_ts)
    current_hour = now.tm_hour
    time_str = time.strftime('%d.%m.%Y %H:%M:%S', now)

    # Otomatik Saat Kontrolleri
    gece_status = "musait" if current_hour >= 10 else "mesgul"
    ekstra_status = "musait" if current_hour >= 13 else "mesgul"

    # Sabit Müsait Hesaplar
    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 9](https://t.me/kabusxkira/49)"
    ]
    
    mesgul_hesaplar = []

    # 1. Ekstra Gece Paketi Hesapları (2, 3, 4) - 13:00'a kadar Meşgul
    ekstra_list = [
        ("[Hesap 2](https://t.me/kabusxkira/10)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 3](https://t.me/kabusxkira/12)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 4](https://t.me/kabusxkira/14)", "Ekstra Gece Paketi Devrede")
    ]
    for link, label in ekstra_list:
        if ekstra_status == "musait":
            musait_hesaplar.append(link)
        else:
            mesgul_hesaplar.append(f"{link} - {label}")

    # 2. Sayaçlı Hesaplar (5, 6)
    hesap5_timer = get_countdown(HESAP5_TARGET_TS)
    if hesap5_timer:
        mesgul_hesaplar.append(f"[Hesap 5](https://t.me/kabusxkira/19) - {hesap5_timer}")
    else:
        musait_hesaplar.append("[Hesap 5](https://t.me/kabusxkira/19)")

    hesap6_timer = get_countdown(HESAP6_TARGET_TS)
    if hesap6_timer:
        mesgul_hesaplar.append(f"[Hesap 6](https://t.me/kabusxkira/22) - {hesap6_timer}")
    else:
        musait_hesaplar.append("[Hesap 6](https://t.me/kabusxkira/22)")

    # 3. Gece Paketi Hesapları (7, 8) - 10:00'a kadar Meşgul
    gece_list = [
        ("[Hesap 7](https://t.me/kabusxkira/34)", "Gece Paketi Devrede"),
        ("[Hesap 8](https://t.me/kabusxkira/40)", "Gece Paketi Devrede")
    ]
    for link, label in gece_list:
        if gece_status == "musait":
            musait_hesaplar.append(link)
        else:
            mesgul_hesaplar.append(f"{link} - {label}")

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

    if MESSAGE_ID is None:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHANNEL_ID,
            "text": text,
            "parse_mode": "Markdown",
            "disable_web_page_preview": True
        }
    else:
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
        if res.get("ok") and MESSAGE_ID is None:
            MESSAGE_ID = res["result"]["message_id"]
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
