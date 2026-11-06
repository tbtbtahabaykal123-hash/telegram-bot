import os
import time
import requests
from datetime import datetime, timezone, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 65

def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 2](https://t.me/kabusxkira/10)",
        "[Hesap 4](https://t.me/kabusxkira/14)",
        "[Hesap 8](https://t.me/kabusxkira/40)",
        "[Hesap 9](https://t.me/kabusxkira/49)"
    ]
    
    mesgul_hesaplar = [
        "[Hesap 3](https://t.me/kabusxkira/12) (Gece Paketi)",
        "[Hesap 5](https://t.me/kabusxkira/19) (Gece Paketi)",
        "[Hesap 6](https://t.me/kabusxkira/22) (Gece Paketi)",
        "[Hesap 7](https://t.me/kabusxkira/34) (Gece Paketi)"
    ]

    musait_text = "\n".join(musait_hesaplar)
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
    if not BOT_
