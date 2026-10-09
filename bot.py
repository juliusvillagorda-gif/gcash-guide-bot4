
import os
import time
import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API = f"https://api.telegram.org/bot{TOKEN}"

MESSAGES = {
    "/start": (
        "Welcome sa GCash Guide Bot!\n\n"
        "/register - Registration guide\n"
        "/verify - Verification guide\n"
        "/help - Mga command"
    ),
    "/register": (
        "Para mag-register, buksan ang opisyal na GCash app "
        "at sundin ang instructions nito.\n\n"
        "Website: https://www.gcash.com/\n"
        "Gamitin lamang ang sarili mong impormasyon."
    ),
    "/verify": (
        "Sundin ang verification instructions sa opisyal na "
        "GCash app. Huwag ibahagi ang OTP, MPIN, o password."
    ),
    "/help": (
        "/start - Simulan\n"
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
                params={"timeout": 25, "offset": offset},
                timeout=35,
            )
            response.raise_for_status()

            for update in response.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message", {})
                chat = message.get("chat", {})
                chat_id = chat.get("id")
                command = message.get("text", "").strip().lower()

                if not chat_id or not command:
                    continue

                reply = MESSAGES.get(
                    command,
                    "Hindi kilalang command. I-type ang /help."
                )
                send_message(chat_id, reply)

        except (requests.RequestException, ValueError) as error:
            print(f"Temporary error: {error}")
            time.sleep(5)


if __name__ == "__main__":
    main()
