
import os
import time
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise RuntimeError("Missing TELEGRAM_BOT_TOKEN environment variable")

API = f"https://api.telegram.org/bot{TOKEN}"

def telegram(method, data=None, timeout=35):
    response = requests.post(
        f"{API}/{method}",
        json=data or {},
        timeout=timeout
    )
    response.raise_for_status()
    result = response.json()

    if not result.get("ok"):
        raise RuntimeError(result.get("description", "Telegram API error"))

    return result["result"]

def send_message(chat_id, text, keyboard=None):
    payload = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        payload["reply_markup"] = {
            "inline_keyboard": keyboard
        }

    telegram("sendMessage", payload)

def main_menu():
    return [
        [
            {"text": "👤 Sample ng Pangalan", "callback_data": "name"},
            {"text": "🏠 Sample ng Address", "callback_data": "address"}
        ],
        [
            {"text": "📅 Sample ng Birthday", "callback_data": "birth"},
            {"text": "📋 Registration Guide", "callback_data": "guide"}
        ],
        [
            {"text": "❓ Help", "callback_data": "help"}
        ]
    ]

def show_sample(chat_id, choice):
    samples = {
        "name": (
            "👤 SAMPLE NG PANGALAN\n\n"
            "First name: Juan\n"
            "Middle name: Dela\n"
            "Last name: Cruz\n\n"
            "Kathang-isip na halimbawa lamang. "
            "Gamitin ang pangalan ayon sa sarili mong opisyal na dokumento."
        ),
        "address": (
            "🏠 SAMPLE NG ADDRESS\n\n"
            "House number: 123\n"
            "Street: Sample Street\n"
            "City: Sample City\n\n"
            "Kathang-isip na address ito. "
            "Ilagay ang sarili mong tunay na address sa opisyal na app."
        ),
        "birth": (
            "📅 SAMPLE NG BIRTHDAY\n\n"
            "Halimbawa: 01/15/2000\n\n"
            "Kathang-isip na petsa lamang. "
            "Gamitin ang sarili mong tamang petsa ng kapanganakan "
            "at sundin ang format sa app."
        ),
        "guide": (
            "📋 REGISTRATION GUIDE\n\n"
            "1. Buksan ang opisyal na GCash app.\n"
            "2. Sundin ang registration instructions.\n"
            "3. Ilagay ang sarili mong impormasyon.\n"
            "4. Kumpletuhin ang verification sa opisyal na app.\n\n"
            "Help Center: https://help.gcash.com/\n\n"
            "Huwag ibahagi sa bot ang OTP, MPIN, password, o ID."
        ),
        "help": (
            "❓ MGA PAGPIPILIAN\n\n"
            "Pumili ng button sa ibaba para makita ang sample.\n"
            "I-type ang /start upang bumalik sa menu."
        )
    }

    send_message(
        chat_id,
        samples.get(choice, "Hindi available ang sample na ito."),
        main_menu()
    )

def handle_update(update):
    if "callback_query" in update:
        query = update["callback_query"]
        chat_id = query["message"]["chat"]["id"]
        choice = query.get("data", "")

        telegram("answerCallbackQuery", {
            "callback_query_id": query["id"]
        })

        show_sample(chat_id, choice)
        return

    message = update.get("message", {})
    chat = message.get("chat", {})
    chat_id = chat.get("id")
    text = message.get("text", "").strip().lower()

    if not chat_id:
        return

    if text.startswith("/start"):
        send_message(
            chat_id,
            "Kumusta! 👋\n\n"
            "Welcome sa GCash Registration Sample Bot.\n"
            "Pumili ng sample sa buttons sa ibaba.\n\n"
            "Ang mga detalye ay kathang-isip lamang. "
            "Hindi kami opisyal na GCash support.",
            main_menu()
        )
    elif text.startswith("/help"):
        show_sample(chat_id, "help")
    else:
        send_message(
            chat_id,
            "Pindutin ang isang button para makita ang sample, "
            "o i-type ang /start para bumalik sa menu.",
            main_menu()
        )

def main():
    bot = telegram("getMe")
    print("Bot connected:", bot.get("username", "unknown"))

    webhook = telegram("getWebhookInfo")
    if webhook.get("url"):
        raise RuntimeError(
            "May naka-set na webhook. Alisin ito sa bot setup "
            "bago gumamit ng polling."
        )

    offset = 0
    print("Bot is running...")

    while True:
        try:
            updates = telegram(
                "getUpdates",
                {
                    "offset": offset,
                    "timeout": 25,
                    "allowed_updates": ["message", "callback_query"]
                },
                timeout=35
            )

            for update in updates:
                offset = update["update_id"] + 1

                try:
                    handle_update(update)
                except Exception as exc:
                    print("Update handling error:", str(exc))

        except (requests.RequestException, RuntimeError) as exc:
            print("Telegram connection error:", str(exc))
            time.sleep(5)

if __name__ == "__main__":
    main()
