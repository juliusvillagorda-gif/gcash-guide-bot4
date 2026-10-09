import os
import time
import requests

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("I-set ang TELEGRAM_BOT_TOKEN sa environment variables.")

API = f"https://api.telegram.org/bot{TOKEN}"

# Kathang-isip na sample data lamang. Huwag gamitin bilang totoong identity.
SAMPLES = [
    {"pangalan": "Juan", "gitna": "Dela Cruz", "apelyido": "Santos", "address": "123 Halimbawang Street, Barangay Sample, Lungsod Halimbawa", "birthday": "15 Enero 1998"},
    {"pangalan": "Maria", "gitna": "Reyes", "apelyido": "Dela Cruz", "address": "45 Ulirang Road, Barangay Pag-asa, Bayan Halimbawa", "birthday": "22 Marso 1997"},
    {"pangalan": "Pedro", "gitna": "Garcia", "apelyido": "Ramos", "address": "8 Sampaguita Lane, Barangay Masaya, Lungsod Halimbawa", "birthday": "03 Abril 1995"},
    {"pangalan": "Ana", "gitna": "Lopez", "apelyido": "Mendoza", "address": "77 Rosal Street, Barangay Mabini, Bayan Halimbawa", "birthday": "11 Mayo 2001"},
    {"pangalan": "Jose", "gitna": "Aquino", "apelyido": "Flores", "address": "16 Maligaya Avenue, Barangay Malinis, Lungsod Halimbawa", "birthday": "27 Hunyo 1996"},
    {"pangalan": "Liza", "gitna": "Castro", "apelyido": "Navarro", "address": "29 Ilang-Ilang Street, Barangay Bagong Araw, Bayan Halimbawa", "birthday": "09 Hulyo 1999"},
    {"pangalan": "Marco", "gitna": "Torres", "apelyido": "Villanueva", "address": "51 Mabuhay Road, Barangay Pagkakaisa, Lungsod Halimbawa", "birthday": "14 Agosto 1994"},
    {"pangalan": "Rosa", "gitna": "Bautista", "apelyido": "Morales", "address": "62 Liwayway Street, Barangay Malaya, Bayan Halimbawa", "birthday": "30 Setyembre 2000"},
    {"pangalan": "Daniel", "gitna": "Cruz", "apelyido": "Santiago", "address": "10 Masinop Lane, Barangay Masagana, Lungsod Halimbawa", "birthday": "05 Oktubre 1993"},
    {"pangalan": "Elena", "gitna": "Rivera", "apelyido": "Gonzales", "address": "88 Pag-asa Street, Barangay Payapa, Bayan Halimbawa", "birthday": "19 Nobyembre 1998"},
    {"pangalan": "Miguel", "gitna": "Perez", "apelyido": "Aquino", "address": "24 Mabini Avenue, Barangay Maunlad, Lungsod Halimbawa", "birthday": "07 Disyembre 1997"},
    {"pangalan": "Sofia", "gitna": "Ramos", "apelyido": "Castillo", "address": "35 Malinis Street, Barangay Maligaya, Bayan Halimbawa", "birthday": "12 Enero 2002"},
    {"pangalan": "Andres", "gitna": "Flores", "apelyido": "Diaz", "address": "19 Sampaguita Road, Barangay Bagong Buhay, Lungsod Halimbawa", "birthday": "25 Pebrero 1996"},
    {"pangalan": "Clara", "gitna": "Mendoza", "apelyido": "Reyes", "address": "70 Rosal Lane, Barangay Matatag, Bayan Halimbawa", "birthday": "16 Marso 1999"},
    {"pangalan": "Ramon", "gitna": "Navarro", "apelyido": "Garcia", "address": "42 Ilang-Ilang Avenue, Barangay Pag-unlad, Lungsod Halimbawa", "birthday": "08 Abril 1992"},
    {"pangalan": "Nina", "gitna": "Villanueva", "apelyido": "Lopez", "address": "13 Liwayway Road, Barangay Masikap, Bayan Halimbawa", "birthday": "21 Mayo 2001"},
    {"pangalan": "Paolo", "gitna": "Morales", "apelyido": "Torres", "address": "96 Maligaya Street, Barangay Mapayapa, Lungsod Halimbawa", "birthday": "02 Hunyo 1995"},
    {"pangalan": "Bea", "gitna": "Santiago", "apelyido": "Bautista", "address": "57 Pag-asa Lane, Barangay Malinis, Bayan Halimbawa", "birthday": "18 Hulyo 2000"},
    {"pangalan": "Carlo", "gitna": "Gonzales", "apelyido": "Perez", "address": "31 Mabuhay Street, Barangay Masagana, Lungsod Halimbawa", "birthday": "29 Agosto 1994"},
    {"pangalan": "Mila", "gitna": "Castillo", "apelyido": "Rivera", "address": "64 Sampaguita Avenue, Barangay Bagong Araw, Bayan Halimbawa", "birthday": "10 Setyembre 1998"},
    {"pangalan": "Ernesto", "gitna": "Diaz", "apelyido": "Aquino", "address": "22 Rosal Road, Barangay Payapa, Lungsod Halimbawa", "birthday": "06 Oktubre 1991"},
    {"pangalan": "Joy", "gitna": "Reyes", "apelyido": "Flores", "address": "49 Liwayway Lane, Barangay Pag-asa, Bayan Halimbawa", "birthday": "23 Nobyembre 2002"},
    {"pangalan": "Noel", "gitna": "Santos", "apelyido": "Mendoza", "address": "11 Mabini Street, Barangay Malaya, Lungsod Halimbawa", "birthday": "17 Disyembre 1993"},
    {"pangalan": "Irene", "gitna": "Garcia", "apelyido": "Torres", "address": "83 Masinop Avenue, Barangay Matatag, Bayan Halimbawa", "birthday": "04 Enero 1997"},
    {"pangalan": "Luis", "gitna": "Lopez", "apelyido": "Navarro", "address": "26 Maligaya Road, Barangay Masikap, Lungsod Halimbawa", "birthday": "20 Pebrero 1996"},
    {"pangalan": "Diana", "gitna": "Ramos", "apelyido": "Perez", "address": "38 Sampaguita Street, Barangay Pagkakaisa, Bayan Halimbawa", "birthday": "13 Marso 2001"},
    {"pangalan": "Arman", "gitna": "Bautista", "apelyido": "Cruz", "address": "59 Ilang-Ilang Road, Barangay Mabini, Lungsod Halimbawa", "birthday": "26 Abril 1995"},
    {"pangalan": "Faith", "gitna": "Rivera", "apelyido": "Santiago", "address": "72 Rosal Avenue, Barangay Bagong Buhay, Bayan Halimbawa", "birthday": "01 Mayo 2000"},
    {"pangalan": "Ben", "gitna": "Morales", "apelyido": "Castro", "address": "14 Payapa Street, Barangay Maunlad, Lungsod Halimbawa", "birthday": "24 Hunyo 1992"},
    {"pangalan": "Grace", "gitna": "Aquino", "apelyido": "Villanueva", "address": "91 Mabuhay Lane, Barangay Maligaya, Bayan Halimbawa", "birthday": "15 Hulyo 1999"},
    {"pangalan": "Rico", "gitna": "Mendoza", "apelyido": "Gonzales", "address": "33 Pag-asa Road, Barangay Masagana, Lungsod Halimbawa", "birthday": "28 Agosto 1994"},
    {"pangalan": "Ella", "gitna": "Torres", "apelyido": "Diaz", "address": "47 Sampaguita Lane, Barangay Malinis, Bayan Halimbawa", "birthday": "09 Setyembre 2002"},
    {"pangalan": "Nestor", "gitna": "Perez", "apelyido": "Reyes", "address": "65 Liwayway Avenue, Barangay Payapa, Bayan Halimbawa", "birthday": "18 Oktubre 1990"},
    {"pangalan": "Lourdes", "gitna": "Castro", "apelyido": "Santos", "address": "28 Mabini Road, Barangay Pag-unlad, Lungsod Halimbawa", "birthday": "07 Nobyembre 1997"},
    {"pangalan": "Gabriel", "gitna": "Navarro", "apelyido": "Ramos", "address": "54 Masinop Street, Barangay Mapayapa, Bayan Halimbawa", "birthday": "12 Disyembre 1996"},
    {"pangalan": "Mara", "gitna": "Flores", "apelyido": "Rivera", "address": "17 Ilang-Ilang Lane, Barangay Bagong Araw, Lungsod Halimbawa", "birthday": "03 Enero 2001"},
    {"pangalan": "Felix", "gitna": "Santiago", "apelyido": "Morales", "address": "86 Rosal Road, Barangay Malaya, Bayan Halimbawa", "birthday": "22 Pebrero 1993"},
    {"pangalan": "Celia", "gitna": "Diaz", "apelyido": "Bautista", "address": "39 Mabuhay Avenue, Barangay Matatag, Bayan Halimbawa", "birthday": "14 Marso 1998"},
    {"pangalan": "Anton", "gitna": "Gonzales", "apelyido": "Castillo", "address": "21 Pag-asa Street, Barangay Masikap, Lungsod Halimbawa", "birthday": "30 Abril 1995"},
    {"pangalan": "Lani", "gitna": "Perez", "apelyido": "Aquino", "address": "68 Sampaguita Road, Barangay Mabini, Bayan Halimbawa", "birthday": "11 Mayo 2000"},
    {"pangalan": "Oscar", "gitna": "Villanueva", "apelyido": "Lopez", "address": "12 Liwayway Street, Barangay Masagana, Lungsod Halimbawa", "birthday": "25 Hunyo 1991"},
    {"pangalan": "Tina", "gitna": "Cruz", "apelyido": "Garcia", "address": "93 Rosal Lane, Barangay Pagkakaisa, Bayan Halimbawa", "birthday": "08 Hulyo 1999"},
    {"pangalan": "Rafael", "gitna": "Santos", "apelyido": "Rivera", "address": "44 Maligaya Avenue, Barangay Payapa, Lungsod Halimbawa", "birthday": "16 Agosto 1994"},
    {"pangalan": "Aira", "gitna": "Reyes", "apelyido": "Navarro", "address": "27 Mabini Lane, Barangay Bagong Buhay, Bayan Halimbawa", "birthday": "02 Setyembre 2002"},
    {"pangalan": "Simon", "gitna": "Mendoza", "apelyido": "Perez", "address": "58 Ilang-Ilang Street, Barangay Maunlad, Lungsod Halimbawa", "birthday": "19 Oktubre 1996"},
    {"pangalan": "Luna", "gitna": "Castillo", "apelyido": "Torres", "address": "36 Pag-asa Avenue, Barangay Malinis, Bayan Halimbawa", "birthday": "05 Nobyembre 2001"},
    {"pangalan": "Emilio", "gitna": "Bautista", "apelyido": "Diaz", "address": "79 Sampaguita Road, Barangay Malaya, Bayan Halimbawa", "birthday": "23 Disyembre 1992"},
    {"pangalan": "Patricia", "gitna": "Garcia", "apelyido": "Flores", "address": "18 Liwayway Street, Barangay Matatag, Bayan Halimbawa", "birthday": "06 Enero 1998"},
    {"pangalan": "Adrian", "gitna": "Rivera", "apelyido": "Santiago", "address": "52 Mabuhay Road, Barangay Masikap, Lungsod Halimbawa", "birthday": "17 Marso 1995"},
    {"pangalan": "May", "gitna": "Torres", "apelyido": "Ramos", "address": "41 Rosal Street, Barangay Pag-asa, Bayan Halimbawa", "birthday": "28 Hulyo 2000"},
]


# Randomized fictional values: each click can produce a new combination.
FIRST_NAMES = [
    "Juan", "Maria", "Pedro", "Ana", "Jose", "Liza", "Marco", "Rosa", "Daniel", "Elena",
    "Miguel", "Sofia", "Andres", "Clara", "Ramon", "Nina", "Paolo", "Bea", "Carlo", "Mila",
    "Ernesto", "Joy", "Noel", "Irene", "Luis", "Diana", "Arman", "Faith", "Ben", "Grace",
    "Rico", "Ella", "Nestor", "Lourdes", "Gabriel", "Mara", "Felix", "Celia", "Anton", "Lani",
    "Oscar", "Tina", "Rafael", "Aira", "Simon", "Luna", "Emilio", "Patricia", "Adrian", "May"
]
MIDDLE_NAMES = [
    "Dela Cruz", "Reyes", "Garcia", "Lopez", "Aquino", "Castro", "Torres", "Bautista",
    "Rivera", "Perez", "Ramos", "Mendoza", "Navarro", "Villanueva", "Morales", "Santiago",
    "Flores", "Gonzales", "Diaz", "Santos"
]
LAST_NAMES = [
    "Santos", "Dela Cruz", "Ramos", "Mendoza", "Flores", "Navarro", "Villanueva", "Morales",
    "Santiago", "Gonzales", "Aquino", "Castillo", "Rivera", "Perez", "Torres", "Bautista",
    "Garcia", "Reyes", "Castro", "Diaz"
]
STREETS = [
    "Halimbawang Street", "Ulirang Road", "Sampaguita Lane", "Rosal Street", "Maligaya Avenue",
    "Mabini Road", "Ilang-Ilang Street", "Liwayway Lane", "Pag-asa Avenue", "Masinop Road",
    "Mabuhay Street", "Payapa Lane", "Bagong Buhay Road", "Masagana Street", "Mapayapa Avenue"
]
BARANGAYS = [
    "Barangay Sample", "Barangay Halimbawa", "Barangay Pag-asa", "Barangay Masaya",
    "Barangay Mabini", "Barangay Malinis", "Barangay Bagong Araw", "Barangay Pagkakaisa",
    "Barangay Malaya", "Barangay Masagana", "Barangay Payapa", "Barangay Maunlad"
]
MONTHS = [
    "Enero", "Pebrero", "Marso", "Abril", "Mayo", "Hunyo",
    "Hulyo", "Agosto", "Setyembre", "Oktubre", "Nobyembre", "Disyembre"
]

def random_fictional_sample():
    import random
    return {
        "pangalan": random.choice(FIRST_NAMES),
        "gitna": random.choice(MIDDLE_NAMES),
        "apelyido": random.choice(LAST_NAMES),
        "address": (
            f"{random.randint(1, 999)} {random.choice(STREETS)}, "
            f"{random.choice(BARANGAYS)}, Lungsod Halimbawa"
        ),
        "birthday": f"{random.randint(1, 28):02d} {random.choice(MONTHS)} {random.randint(1985, 2004)}",
    }

def random_sample_text():
    item = random_fictional_sample()
    return (
        "🎲 BAGONG RANDOM SAMPLE\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "👤 PANGALAN\n"
        f"   First name:  {item['pangalan']}\n"
        f"   Middle name: {item['gitna']}\n"
        f"   Apelyido:    {item['apelyido']}\n\n"
        "🏠 ADDRESS\n"
        f"   {item['address']}\n\n"
        "🎂 BIRTHDAY\n"
        f"   {item['birthday']}\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚠️ Kathang-isip lamang ang sample na ito.\n"
        "Huwag gamitin bilang totoong personal na impormasyon.\n\n"
        "🔀 Pindutin ang “I-shuffle ulit” para sa bagong sample."
    )

def api(method, payload=None, timeout=35):
    response = requests.post(f"{API}/{method}", json=payload or {}, timeout=timeout)
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram API error sa {method}: {data}")
    return data["result"]

def send_message(chat_id, text, keyboard=None):
    payload = {"chat_id": chat_id, "text": text}
    if keyboard:
        payload["reply_markup"] = {"inline_keyboard": keyboard}
    api("sendMessage", payload)

def main_menu():
    return [
        [{"text": "🎲 Random Sample", "callback_data": "random_sample"}],
        [{"text": "✍️ Sample ng Pangalan", "callback_data": "name"},
         {"text": "🏠 Sample ng Address", "callback_data": "address"}],
        [{"text": "🎂 Sample ng Birthday", "callback_data": "birthday"}],
        [{"text": "📖 Registration Guide", "callback_data": "guide"}],
        [{"text": "❓ FAQ", "callback_data": "faq"}],
    ]

def sample_text(item, number):
    return (
        f"📋 SAMPLE #{number} — KATHANG-ISIP LAMANG\n\n"
        f"Pangalan: {item['pangalan']}\n"
        f"Gitnang pangalan: {item['gitna']}\n"
        f"Apelyido: {item['apelyido']}\n"
        f"Address: {item['address']}\n"
        f"Birthday: {item['birthday']}\n\n"
        "Paalala: Huwag kopyahin ang sample bilang sariling impormasyon. "
        "Sa opisyal na registration, gamitin lamang ang sarili mong tamang detalye."
    )

def guide_text():
    return (
        "📖 GABAY SA REGISTRATION\n\n"
        "1. Buksan ang opisyal na GCash app o opisyal na website/help center.\n"
        "2. Piliin ang registration/sign-up at sundin ang kasalukuyang mga tagubilin sa app.\n"
        "3. Ilagay ang sarili mong tamang impormasyon; tiyaking tugma ito sa iyong dokumento kung hinihingi.\n"
        "4. Basahin ang mga tuntunin at privacy notice bago magpatuloy.\n"
        "5. Kung may problema, gamitin ang opisyal na Help Center.\n\n"
        "Hindi opisyal na GCash bot ang gabay na ito. Hindi ito gumagawa ng account."
    )

def faq_text():
    return (
        "❓ MGA KARANIWANG TANONG (FAQ)\n\n"
        "1. Totoo ba ang 50 sample? Hindi. Lahat ay kathang-isip para sa pagsasanay.\n\n"
        "2. Maaari bang gamitin ang sample sa registration? Hindi. Gamitin ang sarili mong tamang detalye.\n\n"
        "3. Hihingi ba ang bot ng OTP, MPIN, password o ID? Hindi kailanman.\n\n"
        "4. Saan ako magpaparehistro? Sa opisyal na GCash app at mga opisyal na channel lamang.\n\n"
        "5. Ano ang gagawin kung may error? Tingnan ang mensahe sa app at makipag-ugnayan sa opisyal na GCash Help Center.\n\n"
        "6. Dapat bang ibigay ang OTP o MPIN sa admin? Hindi. Huwag ibahagi sa sinuman."
    )

def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip().lower()
    if text in ("/start", "/help", "menu"):
        send_message(
            chat_id,
            "Kumusta! 👋 Ito ay GCash registration guide na may kathang-isip na samples.\n\n"
            "Pumili sa menu sa ibaba. Huwag ipadala rito ang totoong personal na detalye, "
            "OTP, MPIN, password, o ID.",
            main_menu()
        )
    else:
        send_message(chat_id, "Piliin ang isang opsyon sa menu o i-type ang /start.", main_menu())

def handle_callback(callback):
    callback_id = callback["id"]
    data = callback.get("data", "")
    chat_id = callback["message"]["chat"]["id"]
    message_id = callback["message"]["message_id"]

    api("answerCallbackQuery", {"callback_query_id": callback_id})

    if data in ("samples", "random_sample"):
        send_message(chat_id, random_sample_text(), [
            [{"text": "🔀 I-shuffle ulit", "callback_data": "random_sample"}],
            [{"text": "✍️ Random na Pangalan", "callback_data": "name"},
             {"text": "🏠 Random na Address", "callback_data": "address"}],
            [{"text": "🎂 Random na Birthday", "callback_data": "birthday"}],
            [{"text": "⬅️ Menu", "callback_data": "menu"}]
        ])
    elif data == "name":
        import random
        item = random_fictional_sample()
        send_message(chat_id,
            "✍️ RANDOM NA PANGALAN — KATHANG-ISIP LAMANG\n\n"
            f"Pangalan: {item['pangalan']}\nGitnang pangalan: {item['gitna']}\nApelyido: {item['apelyido']}\n\n"
            "Pindutin ulit ang Random na Pangalan para sa bagong kombinasyon.",
            [[{"text": "🔀 Random na Pangalan ulit", "callback_data": "name"}],
             [{"text": "⬅️ Menu", "callback_data": "menu"}]])
    elif data == "address":
        item = random_fictional_sample()
        send_message(chat_id,
            "🏠 RANDOM NA ADDRESS — KATHANG-ISIP LAMANG\n\n"
            f"{item['address']}\n\n"
            "Pindutin ulit para sa bagong halimbawa. Huwag gamitin bilang totoong address.",
            [[{"text": "🔀 Random na Address ulit", "callback_data": "address"}],
             [{"text": "⬅️ Menu", "callback_data": "menu"}]])
    elif data == "birthday":
        item = random_fictional_sample()
        send_message(chat_id,
            "🎂 RANDOM NA BIRTHDAY — KATHANG-ISIP LAMANG\n\n"
            f"{item['birthday']}\n\n"
            "Pindutin ulit para sa ibang format/example. Para sa totoong registration, sariling tamang birthday lamang.",
            [[{"text": "🔀 Random na Birthday ulit", "callback_data": "birthday"}],
             [{"text": "⬅️ Menu", "callback_data": "menu"}]])
    elif data == "guide":
        send_message(chat_id, guide_text(), main_menu())
    elif data == "faq":
        send_message(chat_id, faq_text(), main_menu())
    elif data == "menu":
        send_message(chat_id, "Piliin ang gusto mong tingnan:", main_menu())
    else:
        send_message(chat_id, "Hindi ko nakilala ang opsyon. I-type ang /start.", main_menu())

def main():
    print("Bot is running...")
    # Long polling ay hindi gagana kung naka-set pa ang webhook.
    info = api("getWebhookInfo")
    if info.get("url"):
        raise RuntimeError(
            "May naka-set pang Telegram webhook. Alisin ito bago gumamit ng polling: "
            f"{API}/deleteWebhook?drop_pending_updates=true"
        )

    offset = None
    while True:
        try:
            payload = {"timeout": 25}
            if offset is not None:
                payload["offset"] = offset
            updates = api("getUpdates", payload, timeout=35)
            for update in updates:
                offset = update["update_id"] + 1
                if "message" in update:
                    handle_message(update["message"])
                elif "callback_query" in update:
                    handle_callback(update["callback_query"])
        except KeyboardInterrupt:
            print("Bot stopped.")
            break
        except Exception as exc:
            print(f"May error: {exc}")
            time.sleep(3)

if __name__ == "__main__":
    main()
