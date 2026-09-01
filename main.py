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

# Telegram Ayarları
BOT_TOKEN = "7724395805:AAEUh-4o3M-Y87w-5O-E01c1q2V3y4Z5"
CHANNEL_ID = "@btkabus"
MESSAGE_ID = 1234

bot = Bot(token=BOT_TOKEN)

def get_turkey_time():
    tz = pytz.timezone('Europe/Istanbul')
    return datetime.now(tz)

def generate_status_text():
    now = get_turkey_time()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%d.%m.%Y")
    
    text = f"""🔥 **BT KABUS HESAP KİRALAMA SERVİSİ** 🔥
📅 **Tarih:** {date_str} | ⏰ **Saat:** {time_str}

━━━━━━━━━━━━━━━━━━━━━━
🟢 **LİSTE 1:** MÜSAİT
🌙 **LİSTE 2:** EKSTRA GECE PAKETİ DEVREDE
🌙 **LİSTE 3:** EKSTRA GECE PAKETİ DEVREDE
🌙 **LİSTE 4:** EKSTRA GECE PAKETİ DEVREDE
🌙 **LİSTE 5:** EKSTRA GECE PAKETİ DEVREDE
🌙 **LİSTE 6:** EKSTRA GECE PAKETİ DEVREDE
🌙 **LİSTE 7:** EKSTRA GECE PAKETİ DEVREDE
━━━━━━━━━━━━━━━━━━━━━━

ℹ️ Hesap kiralamak ve detaylı bilgi almak için iletişime geçebilirsiniz."""
    return text

async def update_loop():
    while True:
        try:
            new_text = generate_status_text()
            await bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=MESSAGE_ID,
                text=new_text,
                parse_mode='Markdown'
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
