import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

BOT_TOKEN = "9180537800:AAFE0VCxfBhacAiCprvpgQUXZf-gbot0LiQ"
CHANNEL_ID = "@kabusxkira"
MESSAGE_ID = 65

def get_message_text():
    tz_tr = timezone(timedelta(hours=3))
    now_tr = datetime.now(tz_tr)
    time_str = now_tr.strftime('%d.%m.%Y %H:%M:%S')

    musait_hesaplar = [
        "[Hesap 1](https://t.me/kabusxkira/3)",
        "[Hesap 4](https://t.me/kabusxkira/14)",
        "[Hesap 8](https://t.me/kabusxkira/40)"
    ]
    
    mesgul_hesaplar = [
        "[Hesap 2](https://t.me/kabusxkira/10) (Ekstra Gece Paketi)",
        "[Hesap 3](https://t.me/kabusxkira/12) (Ekstra Gece Paketi)",
        "[Hesap 5](https://t.me/kabusxkira/19) (Gece Paketi)",
        "[Hesap 6](https://t.me/kabusxkira/22) (Gece Paketi)",
        "[Hesap 7](https://t.me/kabusxkira/34) - 24s 00dk 00sn kaldı",
        "[Hesap 9](https://t.me/kabusxkira/49) (Gece Paketi)"
    ]

    musait_text = "\n".join(musait_hesaplar) if musait_hesaplar else "Yok"
    mesgul_text = "\n".join(mesgul_hesaplar) if mesgul_hesaplar else "Yok"

    return f"""KABUS RENT

┌──────────────────────┐
  🟢 Müsait Hesaplar
└──────────────────────┘

{musait_text}

┌──────────────────────┐
  🔴 Meşgul Hesaplar
└──────────────────────┘

{mesgul_text}

⏱️ Son Güncelleme: {time_str}

Hesap no'ların üzerine tıklayarak hesaplara hızlı bir şekilde ulaşabilirsiniz.

Hemen kiralamak için;
✅ @btkabus"""

def update_telegram_message():
    if not BOT_TOKEN:
        print("HATA: BOT_TOKEN bulunamadı!")
        return {"error": "Token yok"}

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText"
    payload = {
        "chat_id": CHANNEL_ID,
        "message_id": MESSAGE_ID,
        "text": get_message_text(),
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res = json.loads(response.read().decode('utf-8'))
            print("Telegram Yanıtı:", res)
            return res
    except Exception as e:
        print("Hata:", e)
        return {"error": str(e)}

def auto_loop():
    import time
    time.sleep(5)
    update_telegram_message()
    while True:
        time.sleep(60)
        update_telegram_message()

Thread(target=auto_loop, daemon=True).start()

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        status = update_telegram_message()
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(f"Guncelleme Tetiklendi: {status}".encode('utf-8'))
        
    def log_message(self, format, *args):
        return

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Sunucu {port} portunda çalışıyor...")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
