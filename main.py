import asyncio
import datetime
import os
from threading import Thread
from flask import Flask
from telegram import Bot

# Render Port Taramasını Geçmek İçin Web Sunucusu
app = Flask('')


@app.route('/')
def home():
  return 'Bot Calisiyor!'


def run():
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)


def keep_alive():
  t = Thread(target=run)
  t.start()


# TELEGRAM BOT KODLARI
TOKEN = '8978792663:AAFEmc5qriY8a4tuX05yxzARfEr5KgwIMM0'
CHAT_ID = -1002247545043
MESSAGE_ID = 23

bot = Bot(token=TOKEN)


async def main():
  hedef_tarih = datetime.datetime(2026, 8, 25, 0, 0, 0)

  while True:
    try:
      simdi = datetime.datetime.now()
      fark = hedef_tarih - simdi

      if fark.total_seconds() > 0:
        gun = fark.days
        saat, artan = divmod(fark.seconds, 3600)
        dakika, saniye = divmod(artan, 60)

        metin = (
            f'🟢 **Müsait Hesaplar**\nHesap 6\n\n'
            f'🔴 **Meşgul Hesaplar**\n'
            f'Hesap 1 - {gun}g, {saat}s, {dakika}d, {saniye}s kaldı.\n\n'
            f'🕒 *Son Güncelleme:* {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}'
        )
      else:
        metin = 'Süre doldu!'

      await bot.edit_message_text(
          chat_id=CHAT_ID,
          message_id=MESSAGE_ID,
          text=metin,
          parse_mode='Markdown',
      )
    except Exception as e:
      print(f'Hata: {e}')

    await asyncio.sleep(5)


if __name__ == '__main__':
  keep_alive()
  asyncio.run(main())
