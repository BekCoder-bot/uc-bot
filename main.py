from flask import Flask, request
import telebot
import os
import requests

API_TOKEN = os.environ.get("BOT_TOKEN")
PUBG_API_KEY = os.environ.get("PUBG_API_KEY")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

user_data = {}
admin_id = 1382850686

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

def uc_options_keyboard(lang):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    uc_list = [
        ("60 + 3 UC", 0.89), ("600 + 90 UC", 8.99), ("1500 + 375 UC", 22.49),
        ("3000 + 1000 UC", 44.49), ("6000 + 2400 UC", 89.99), ("12000 + 4800 UC", 179.99),
        ("18000 + 7200 UC", 269.99), ("24000 + 9600 UC", 359.99),
        ("30000 + 12000 UC", 449.99), ("60000 + 24000 UC", 899.99)
    ]
    for i in range(0, len(uc_list), 2):
        btns = []
        for j in range(2):
            if i + j < len(uc_list):
                title, usd = uc_list[i + j]
                so'm = round(usd * 13000)
                rub = round(usd * 83)
                btns.append(f"{title} - ${usd} | {so'm} so'm | {rub} rub")
        markup.add(*btns)
    return markup

def is_valid_pubg_id(nickname):
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={nickname}"
    headers = {
        "Authorization": f"Bearer {PUBG_API_KEY}",
        "Accept": "application/vnd.api+json"
    }
    response = requests.get(url, headers=headers)
    return response.status_code == 200 and len(response.json().get("data", [])) > 0

@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🇺🇿 O'zbekcha", "🇷🇺 Русский", "🇬🇧 English")
    bot.send_message(chat_id, "🇿🇿 Iltimos, tilni tanlang / Please select your language:", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text in ["🇺🇿 O'zbekcha", "🇷🇺 Русский", "🇬🇧 English"])
def language_selected(message):
    chat_id = message.chat.id
    lang = message.text
    user_data[chat_id] = {"lang": lang}
    bot.send_message(chat_id, "UC miqdorini tanlang / Choose UC amount:", reply_markup=uc_options_keyboard(lang))

@bot.message_handler(func=lambda msg: "UC - $" in msg.text)
def uc_selected(message):
    chat_id = message.chat.id
    user_data[chat_id]["uc"] = message.text
    bot.send_message(chat_id, "🔹 Iltimos, PUBG nickname'ingizni kiriting:")
    bot.register_next_step_handler(message, get_pubg_id)

def get_pubg_id(message):
    chat_id = message.chat.id
    nickname = message.text.strip()
    if not is_valid_pubg_id(nickname):
        bot.send_message(chat_id, "❌ PUBG ID topilmadi. Iltimos, to‘g‘ri nickname kiriting.")
        return
    user_data[chat_id]["pubg_id"] = nickname
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✅ To‘lov qilindi")
    bot.send_message(chat_id, "💳 To‘lovni amalga oshiring va '✅ To‘lov qilindi' tugmasini bosing.", reply_markup=markup)

@bot.message_handler(func=lambda msg: msg.text == "✅ To‘lov qilindi")
def payment_done(message):
    chat_id = message.chat.id
    info = user_data.get(chat_id)
    if not info:
        return
    username = message.from_user.username or "Noma'lum"
    msg = (
        f"🆕 Yangi buyurtma:\n"
        f"👤 @{username}\n"
        f"🆔 PUBG ID: {info['pubg_id']}\n"
        f"💸 UC: {info['uc']}"
    )
    bot.send_message(admin_id, msg)
    bot.send_message(chat_id, "✅ Buyurtmangiz qabul qilindi. Tez orada bog‘lanamiz!")

if __name__ == '__main__':
    bot.remove_webhook()
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.set_webhook(url=webhook_url)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
