import os
import time
import requests
from datetime import datetime, timezone, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

# Yeni Bot Tokenı
BOT_TOKEN = "9082460104:AAGndFab45MSz_we1asS89kuNA-E-70gbTE"
CHANNEL_ID = "@kabusxkira"

# Sabit Mesaj ID
MESSAGE_ID = 58

def get_message_text():
    # Türkiye Saati (UTC+3)
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    # 1'den 9'a kadar hepsi Müsait
    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 2](https://t.me/kabusxkira/10)",
        "[Hesap 3](https://t.me/kabusxkira/12)",
        "[Hesap 4](https://t.me/kabusxkira/14)",
        "[Hesap 5](https://t.me/kabusxkira/19)",
        "[Hesap 6](https://t.me/kabusxkira/22)",
        "[Hesap 7](
