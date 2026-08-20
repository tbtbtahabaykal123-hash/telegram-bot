import asyncio
import datetime
import os
from threading import Thread
from flask import Flask
from telegram import Bot

# Render Port Taraması İçin Web Sunucusu
app = Flask('')

@app.route('/')
def home():
    return "Bot Calisiyor!"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# TELEGRAM BOT KODLARI
TOKEN = '8978792663:AAFEmc5qriY8a4tuX05yxzARfEr5KgwIMM0'

# DOĞRU KANAL ID'Sİ
CHAT_ID = -1004315557168

async def main():
    bot = Bot(token=TOKEN)
    hedef_tarih = datetime.datetime(2026, 8, 25, 0, 0, 0)
    message_id = None

    while True:
        try:
            simdi = datetime.datetime.now()
            fark = hedef_tarih - simdi

            if fark.total_seconds() > 0:
                gun = fark.days
                saat, artan = divmod(fark.seconds, 3600)
                dakika, saniye = divmod(artan, 60)
                kalan_sure = f"{gun}g, {saat}s, {dakika}d, {saniye}s"
            else:
                kalan_sure = "Süre doldu!"

            metin = (
                "KABUS RENT\n\n"
                "┌───────────────────┐\n"
                "  🟢 Müsait Hesaplar\n"
                "└───────────────────┘\n\n"
                "  Hesap 1\n"
                "  Hesap 2\n"
                "  Hesap 3\n"
                "  Hesap 4\n"
                "  Hesap 5\n\n"
                "┌───────────────────┐\n"
                "  🔴 Meşgul Hesaplar\n"
                "└───────────────────┘\n\n"
                f"  Hesap 6 - {kalan_sure} kaldı.\n\n"
                f"⏱ Son Güncelleme: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')}\n\n"
                "Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.\n\n"
                "Hemen kiralamak için;\n"
                "✅ @btkabus"
            )

            if message_id is None:
                msg = await bot.send_message(chat_id=CHAT_ID, text=metin)
                message_id = msg.message_id
            else:
                await bot.edit_message_text(chat_id=CHAT_ID, message_id=message_id, text=metin)

        except Exception as e:
            print(f"HATA: {e}")

        await asyncio.sleep(5)

if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
