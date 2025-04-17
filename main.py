from flask import Flask, request
import telebot
import os

API_TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return '', 200
    else:
        return 'Invalid content type', 403

@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, "Salom! Men webhook orqali ishlayapman.")

if __name__ == '__main__':
    bot.remove_webhook()
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    bot.set_webhook(url=webhook_url)
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
