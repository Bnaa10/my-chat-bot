import telebot
from flask import Flask
import threading
import os

# 🔑 APNA DATA YAHAN DAALEIN
TOKEN = "8757250098:AAHKd06LDm4yT4yS-51X_GxlIjffw-8-oFw"
ADMIN_ID = "5554879094"  

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 🌐 Render ko lagna chahiye ki ek website chal rahi hai, isliye ye dummy page banaya hai
@app.route('/')
def index():
    return "Bot is active and running smoothly!"

# 🚀 Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    welcome_text = f"Hi {user_name}. How may I help you?"
    bot.send_message(message.chat.id, welcome_text)

# 📩 Customer ka message jab aapko aaye
@bot.message_handler(func=lambda message: str(message.chat.id) != str(ADMIN_ID))
def handle_customer_message(message):
    admin_text = f"ID: {message.chat.id}\nName: {message.from_user.first_name}\n\n{message.text}"
    bot.send_message(ADMIN_ID, admin_text)

# ↩️ Jab aap (Admin) reply karein
@bot.message_handler(func=lambda message: str(message.chat.id) == str(ADMIN_ID) and message.reply_to_message)
def handle_admin_reply(message):
    try:
        original_text = message.reply_to_message.text
        user_id = original_text.split("\n")[0].replace("ID: ", "").strip()
        bot.send_message(user_id, message.text)
    except Exception as e:
        bot.reply_to(message, "Error: Reply fail ho gaya. Make sure aap 'ID: ...' wale message ko left-swipe karke hi reply kar rahe hain.")

# Bot ko background mein chalane ka function
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # Bot aur Dummy Server dono ko ek sath chalana
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
