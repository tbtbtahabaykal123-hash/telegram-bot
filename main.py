import json
import os
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread

BOT_TOKEN = os.environ.get("BOT_TOKEN", "9180537800:AAFE0VCxfBhacAiCprvpgQUXZf-gbot0LiQ")
CHANNEL_ID = "@kabusxdesh"
MESSAGE_ID = 65


def get_message_text() -> str:
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

    mesgul_hesaplar: list[str] = []

    musait_text = "\n".join(musait_hesaplar) if musait_hesaplar else "Yok"
    mesgul_text = "\n".join(mesgul_hesaplar) if mesgul_hesaplar else "Yok"

    return (
        "KABUS RENT\n\n"
        "┌──────────────────────┐\n"
        "  🟢 Müsait Hesaplar\n"
        "└──────────────────────┘\n\n"
        f"{musait_text}\n\n"
        "┌──────────────────────┐\n"
        "  🔴 Meşgul Hesaplar\n"
        "└──────────────────────┘\n\n"
        f"{mesgul_text}\n\n"
        f"⏱️ Son Güncelleme: {time_str}\n\n"
        "Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.\n\n"
        "Hemen kiralamak için;\n"
        "✅ @btkabus"
    )


def update_telegram_message() -> dict:
    if not BOT_TOKEN:
        print("HATA: BOT_TOKEN tanımlı değil.", flush=True)
        return {"ok": False, "error": "BOT_TOKEN eksik"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": CHANNEL_ID,
        "message_id": MESSAGE_ID,
        "text": get_message_text(),
        "parse_mode": "Markdown",
        "link_preview_options": {"is_disabled": True},
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            res = json.loads(response.read().decode("utf-8"))
            print("Telegram Yanıtı:", res, flush=True)
            return res
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        
