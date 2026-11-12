import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

BOT_TOKEN = "9180537800:AAFE0VCxfBhacAiCprvpgQUXZf-gbot0LiQ"
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 65

def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    musait_hesaplar = []
    
    mesgul_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3) (Gece Paketi)",
        "[Hesap 2](https://t.me/kabusxkira/10) (Gece Paketi)",
        "[Hesap 3](https://t.me/kabusxkira/12) (Gece Paketi)",
        "[Hesap 4](https://t.me/kabusxkira/14) (Gece Paketi)",
        "[Hesap 5](https://t.me/kabusxkira/19) (Gece Paketi)",
        "[Hesap 6](https://t.me/kabusxkira/22) (Gece Paketi)",
        "[Hesap 7](https://t.me/kabusxkira/34) (Gece Paketi)",
        "[Hesap 8](https://t.me/kabusxkira/40) (Gece Paketi)",
        "[Hesap 9](https://t.me/kabusxkira/49) (Gece Paketi)"
    ]

    musait_text = "\n".join(musait_hesaplar) if musait_hesaplar else "Yok"
    mesgul_text = "\n".join(mesgul_hesaplar)

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
        "chat_id
