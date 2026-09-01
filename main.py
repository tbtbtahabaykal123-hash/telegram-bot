import os
import asyncio
from datetime import datetime
import pytz
from flask import Flask
from threading import Thread
from telegram import Bot
from telegram.error import TelegramError

# Flask Web Server
app = Flask('')

@app.route('/')
def home():
    return "Bot Aktif!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Telegram Ayarları (Bot token ve Kanal bilgilerini kendi bilgilerinle doğrula)
BOT_TOKEN = "7724395805:AAEUh-4o3M-Y87w-5O-E01c1q2V3y4Z5"
CHANNEL_ID = "@btkabus"  # veya kanal ID'n
MESSAGE_ID = 1234       # güncellenecek mesaj ID'si

bot = Bot(token=BOT_TOKEN)

def get_turkey_time():
    tz = pytz.timezone('Europe/Istanbul')
    return datetime.now(tz)

def generate_status_text():
    now = get_turkey_time()
    time_str = now.strftime("%d.%m.%Y %H:%M:%S")
    
    text = f"""KABUS RENT

┌──────────────────────┐
🟢 Müsait Hesaplar
└──────────────────────┘

[Hesap 1](https://t.me/kabusxkira/33)
[Hesap 8](https://t.me/kabusxkira/40)

┌──────────────────────┐
🔴 Meşgul Hesaplar
└──────────────────────┘

[Hesap 2](https://t.me/kabusxkira/34) - Ekstra Gece Paketi Devrede
[Hesap 3](https://t.me/kabusxkira/35) - Gece Paketi Devrede
[Hesap 4](https://t.me/kabusxkira/36) - Ekstra Gece Paketi Devrede
[Hesap 5](https://t.me/kabusxkira/37) - Gece Paketi Devrede
[Hesap 6](https://t.me/kabusxkira/38) - Ekstra Gece Paketi Devrede
[Hesap 7](https://t.me/kabusxkira/39) - Ekstra Gece Paketi Devrede

⏱️ Son Güncelleme: {time_str}

Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.

Hemen kiralamak için;
✅ @btkabus"""
    return text

async def update_loop():
    while True:
        try:
            new_text = generate_status_text()
            await bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=MESSAGE_ID,
                text=new_text,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except TelegramError as e:
            print(f"Güncelleme hatası: {e}")
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
            
        await asyncio.sleep(60)

def start_bot_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(update_loop())

if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    start_bot_loop()
