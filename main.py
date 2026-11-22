import os
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN", "9180537800:AAFE0VCxfBhacAiCprvpgQUXZf-gbot0LiQ")
CHANNEL_ID = "@kabusxdesh"
MESSAGE_ID = 65


def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime("%d.%m.%Y %H:%M:%S")

    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxdesh/3)",
        "[Hesap 2](https://t.me/kabusxdesh/10)",
        "[Hesap 3](https://t.me/kabusxdesh/12)",
        "[Hesap 4](https://t.me/kabusxdesh/14)",
        "[Hesap 5](https://t.me/kabusxdesh/19)",
        "[Hesap 6](https://t.me/kabusxdesh/22)",
        "[Hesap 7](https://t.me/kabusxdesh/34)",
        "[Hesap 8](https://t.me/kabusxdesh/40)",
        "[Hesap 9](https://t.me/kabusxdesh/49)",
    ]

    mesgul_hesaplar = []

    musait_text = "\n".join(musait_hesaplar) if musait_hesaplar else "Yok"
    mesgul_text = "\n".join(mesgul_hesaplar) if mesgul_hesaplar else "Yok"

    return (
        "KABUS RENT\n\n"
        "┌──────────────────────┐\n"
        "  🟢 Müsait
