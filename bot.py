
import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API = f"HTTP API:
8482148717:AAEvtRhYOj99pHd5AVhTQ4Iq_hZ357fLyLk"

REGISTRATION_URL = "https://www.gcash.com/"

MESSAGES = {
    "/start": (
        "Welcome sa GCash Registration Guide! 👋\n\n"
        "Pumili ng command:\n"
        "/register - Registration guide\n"
        "/verify - Account verification guide\n"
        "/help - Mga available na command\n\n"
        "Paalala: Gamitin ang sarili mong impormasyon at "
        "ang opisyal na GCash app."
    ),
    "/register": (
        "📱 PAANO MAG-REGISTER\n\n"
        "1. Buksan ang opisyal na GCash app.\n"
        "2. Sundin ang registration instructions.\n"
        "3. Gamitin ang sarili mong mobile number at impormasyon.\n"
        "4. Kumpletuhin ang verification kung kinakailangan.\n\n"
        f"Opisyal na website: {REGISTRATION_URL}\n\n"
        "Hindi gumagawa ng account ang bot na ito."
    ),
    "/verify": (
        "🔐 ACCOUNT VERIFICATION\n\n"
        "Sundin ang verification instructions sa opisyal na "
        "GCash app. Huwag ibahagi sa sinuman ang iyong OTP, "
        "MPIN, password, o identification documents sa chat."
    ),
    "/help": (
        "Available commands:\n"
        "/start - Simulan ang bot\n"
        "/register - Registration guide\n"
        "/verify - Verification guide\n"
        "/help - Tulong"
    ),
}


def send_message(chat_id, text):
    response = requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text},
        timeout=20,
    )
    response.raise_for_status()


def main():
    offset = None
    print("GCash Guide Bot is running.")

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={
                    "timeout": 25,
                    "offset": offset,
                },
                timeout=35,
            )
            response.raise_for_status()

            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                text = message.get("text", "").strip().lower()

                if not chat_id or not text:
                    continue

                reply = MESSAGES.get(
                    text,
                    "Hindi ko maintindihan ang command. "
                    "I-type ang /help para sa mga pagpipilian."
                )
                send_message(chat_id, reply)

        except (requests.RequestException, ValueError) as error:
            print(f"Temporary bot error: {error}")
            time.sleep(5)


if __name__ == "__main__":
    main()
