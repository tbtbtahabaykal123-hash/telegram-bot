import time
import requests

# TELEGRAM BOT VE KANAL AYARLARI
BOT_TOKEN = "8897902804:AAEdFWs9V41gcUipSrE0_n6LPpAz5VOh5D0"
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 47

def update_telegram():
    # Türkiye Saati ve Milisaniye
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
    
    try:
        res = requests.post(url, json=payload, timeout=10)
        print("Telegram Yaniti:", res.json())
    except Exception as e:
        print("Hata:", e)

# Doğrudan sonsuz döngü
while True:
    update_telegram()
    time.sleep(60)
