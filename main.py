import os
import time
import requests
from flask import Flask
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = "8897902804:AAGRP_5WH87wngvCczarPM1w5AF7u-uaAUc"
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 47

def update_telegram_message():
    # Türkiye Saati (UTC+3)
    now_ts = time.time() + (3 * 3600)
    now = time.gmtime(now_ts)
    
    current_hour = now.tm_hour
    time_str = time.strftime('%d.%m.%Y %H:%M:%S', now)
    
    # 1. Gece Paketi Mantığı (Saat 10:00'da Müsait olur)
    # Hesap 3, Hesap 5
    if current_hour >= 10:
        gece_status = "musait"
    else:
        gece_status = "mesgul"

    # 2. Ekstra Gece Paketi Mantığı (Saat 13:00'da Müsait olur)
    # Hesap 2, Hesap 4, Hesap 6, Hesap 7
    if current_hour >= 13:
        ekstra_status = "musait"
    else:
        ekstra_status = "mesgul"

    # Dinamik Liste Oluşturma
    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 8](https://t.me/kabusxkira/40)"
    ]
    mesgul_hesaplar = []

    # Gece Paketi Hesapları Kontrolü
    gece_list = [
        ("[Hesap 3](https://t.me/kabusxkira/12)", "Gece Paketi Devrede"),
        ("[Hesap 5](https://t.me/kabusxkira/19)", "Gece Paketi Devrede")
    ]
    for link, label in gece_list:
        if gece_status == "musait":
            musait_hesaplar.append(link)
        else:
            mesgul_hesaplar.append(f"{link} - {label}")

    # Ekstra Gece Paketi Hesapları Kontrolü
    ekstra_list = [
        ("[Hesap 2](https://t.me/kabusxkira/10)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 4](https://t.me/kabusxkira/14)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 6](https://t.me/kabusxkira/22)", "Ekstra Gece Paketi Devrede"),
        ("[Hesap 7](https://t.me/kabusxkira/34)", "Ekstra Gece Paketi Devrede")
    ]
    for link, label in ekstra_list:
        if ekstra_status == "musait":
            musait_hesaplar.append(link)
        else:
            mesgul_hesaplar.append(f"{link} - {label}")

    # Metin Formatlama
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
