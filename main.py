import asyncio
import datetime
import os
from datetime import timezone, timedelta
from threading import Thread
from flask import Flask
from telegram import Bot
from telegram.constants import ParseMode

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

TOKEN = '8978792663:AAFEmc5qriY8a4tuX05yxzARfEr5KgwIMM0'
CHAT_ID = -1004315557168

async def main():
    bot = Bot(token=TOKEN)
    message_id = None

    # Türkiye Saat Dilimi (UTC+3)
    tr_tz = timezone(timedelta(hours=3))

    while True:
        try:
            # Türkiye saatine göre şu anki zaman
            simdi = datetime.datetime.now(tr_tz)
            
            bugun_11 = simdi.replace(hour=11, minute=0, second=0, microsecond=0)
            bugun_13 = simdi.replace(hour=13, minute=0, second=0, microsecond=0)

            hesaplar = [
                {"isim": "Hesap 1", "link": "https://t.me/kabusxkira/3", "durum": "musait"},
                {"isim": "Hesap 2", "link": "https://t.me/kabusxkira/10", "durum": "ekstra_gece", "bitis": bugun_13},
                {"isim": "Hesap 3", "link": "https://t.me/kabusxkira/12", "durum": "gece", "bitis": bugun_11},
                {"isim": "Hesap 4", "link": "https://t.me/kabusxkira/14", "durum": "ekstra_gece", "bitis": bugun_13},
                {"isim": "Hesap 5", "link": "https://t.me/kabusxkira/19", "durum": "gece", "bitis": bugun_11},
                {"isim": "Hesap 6", "link": "https://t.me/kabusxkira/22", "durum": "ekstra_gece", "bitis": bugun_13}
            ]

            musait_listesi = []
            mesgul_listesi = []

            for h in hesaplar:
                satir_link = f'<a href="{h["link"]}">{h["isim"]}</a>'
                
                if h["durum"] == "musait":
                    musait_listesi.append(f"  {satir_link}")
                
                elif h["durum"] in ["gece", "ekstra_gece"]:
                    if simdi >= h["bitis"]:
                        musait_listesi.append(f"  {satir_link}")
                    else:
                        metin = "Gece Paketi Devrede" if h["durum"] == "gece" else "Ekstra Gece Paketi Devrede"
                        mesgul_listesi.append(f"  {satir_link} - {metin}")

            musait_metin = "\n".join(musait_listesi) if musait_listesi else "  Şu an müsait hesap yok."
            mesgul_metin = "\n".join(mesgul_listesi) if mesgul_listesi else "  Şu an meşgul hesap yok."

            metin = (
                "<b>KABUS RENT</b>\n\n"
                "┌───────────────────┐\n"
                "  🟢 <b>Müsait Hesaplar</b>\n"
                "└───────────────────┘\n\n"
                f"{musait_metin}\n\n"
                "┌───────────────────┐\n"
                "  🔴 <b>Meşgul Hesaplar</b>\n"
                "└───────────────────┘\n\n"
                f"{mesgul_metin}\n\n"
                f"⏱ <i>Son Güncelleme: {simdi.strftime('%d.%m.%Y %H:%M:%S')}</i>\n\n"
                "Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.\n\n"
                "Hemen kiralamak için;\n"
                "✅ @btkabus"
            )

            if message_id is None:
                msg = await bot.send_message(chat_id=CHAT_ID, text=metin, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                message_id = msg.message_id
            else:
                await bot.edit_message_text(chat_id=CHAT_ID, message_id=message_id, text=metin, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

        except Exception as e:
            print(f"HATA: {e}")

        await asyncio.sleep(5)

if __name__ == '__main__':
    keep_alive()
    asyncio.run(main())
