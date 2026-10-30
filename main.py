import os
import time
import requests
from datetime import datetime, timezone, timedelta
from flask import Flask
from threading import Thread

app = Flask(__name__)

# Güncel Bot Tokenı
BOT_TOKEN = "8897902804:AAFwTzAtr1qx6Umzkkig4Jz6GvsdIwVjORQ"
CHANNEL_ID = "@kabusxkira"

# Kilitlenen ve sadece düzenlenecek mesajın ID'si
MESSAGE_ID = 58

def get_message_text():
    # Türkiye Saati (UTC+3)
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    # 1
