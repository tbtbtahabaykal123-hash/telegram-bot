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

# Hesap 6 bitiş zamanı (12s 13dk 26sn geri sayım için başlangıç anından itibaren)
HESAP6_BASLANGIC = datetime.now(timezone(timedelta(hours=3)))
HESAP6_BITIS = HESAP6_BASLANGIC + timedelta(hours=12, minutes=13, seconds=26)


def format_kalan_sure(bitis_zamani, simdi):
    kalan = bitis_zamani - simdi
    toplam_sn = int(kalan.total_seconds())
    if toplam_sn <= 0:
        return "Süresi Doldu"
    saat = toplam_sn // 3600
    dakika = (toplam_sn % 3600) // 60
    saniye = toplam_sn % 60
    return f"{saat}s {dakika}dk {saniye}sn"


def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime("%d.%m.%Y %H:%M:%S")
    hesap6_kalan = format_kalan_sure(HESAP6_BITIS, now_tr)

    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxdesh/3)",
        "[Hesap 2](https://t.me/kabusxdesh/10)",
        "[Hesap 3](https
