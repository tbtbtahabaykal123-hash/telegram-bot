import os
from threading import Thread
from flask import Flask

app = Flask('')


@app.route('/')
def home():
  return 'Bot Calisiyor!'


def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()import asyncio
import datetime
from telegram import Bot

TOKEN = "8978792663:AAFEmc5qriY8a4tuX05yxzARfEr5KgwIMMO"
CHAT_ID = "@kabusxkira"
MESSAGE_ID = 23

bot = Bot(token=TOKEN)

async def main():
    bitis_zamani = datetime.datetime.now() + datetime.timedelta(days=7, hours=22)

    while True:
        try:
            kalan = bitis_zamani - datetime.datetime.now()
            gun = kalan.days
            saat, artan = divmod(kalan.seconds, 3600)
            dakika, saniye = divmod(artan, 60)

            metin = (
                f"🟢 **Müsait Hesaplar**\nHesap 6\n\n"
                f"🔴 **Meşgul Hesaplar**\n"
                f"Hesap 1 - {gun}g, {saat}s, {dakika}d, {saniye}s kaldı.\n\n"
                f"🕒 *Son Güncelleme:* {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
            )

            await bot.edit_message_text(
                chat_id=CHAT_ID,
                message_id=MESSAGE_ID,
                text=metin,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Hata: {e}")
            
        await asyncio.sleep(5)

asyncio.run(main())
