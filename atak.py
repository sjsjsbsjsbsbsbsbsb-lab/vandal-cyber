import telebot
from telebot import types
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor

BOT_TOKEN = "8246012366:AAFCOY7aXRgPqDvWbrNBGgSa-QnDo0nAYes"
ADMIN_ID = 6306318818

bot = telebot.TeleBot(BOT_TOKEN, threaded=True)

# ---------------- داده‌ها ----------------
enemies = {}       # {chat_id: [reply_message_id]}
spam_texts = []
spam_interval = 1  # فاصله پیش‌فرض بین پیام‌ها (ثانیه)

# ---------------- ذخیره / لود ----------------
def save_data():
    with open("bot_data.json", "w") as f:
        json.dump({"enemies": enemies, "spam_texts": spam_texts, "spam_interval": spam_interval}, f)

def load_data():
    global enemies, spam_texts, spam_interval
    try:
        with open("bot_data.json", "r") as f:
            data = json.load(f)
            enemies = data.get("enemies", {})
            spam_texts = data.get("spam_texts", [])
            spam_interval = data.get("spam_interval", 1)
    except:
        enemies = {}
        spam_texts = []
        spam_interval = 1

# ---------------- اسپم ----------------
executor = ThreadPoolExecutor(max_workers=10)

def spam_loop(chat_id, msg_id):
    while msg_id in enemies.get(str(chat_id), []):
        if not spam_texts:
            time.sleep(1)
            continue
        try:
            bot.send_message(
                chat_id,
                random.choice(spam_texts),
                reply_to_message_id=msg_id
            )
            time.sleep(spam_interval)
        except:
            time.sleep(1)

def start_spam(chat_id, msg_id):
    executor.submit(spam_loop, chat_id, msg_id)

# ---------------- پنل ادمین (PV) ----------------
def admin_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("➕ افزودن متن", callback_data="add"),
        types.InlineKeyboardButton("📜 لیست متن‌ها", callback_data="list"),
        types.InlineKeyboardButton("❌ حذف متن", callback_data="remove"),
        types.InlineKeyboardButton("⏱️ تنظیم فاصله", callback_data="interval")
    )
    return kb

@bot.message_handler(commands=["start"])
def start(message):
    if message.from_user.id == ADMIN_ID and message.chat.type == "private":
        bot.send_message(message.chat.id, "پنل مدیریت", reply_markup=admin_menu())

@bot.callback_query_handler(func=lambda c: True)
def panel(call):
    global spam_interval
    if call.from_user.id != ADMIN_ID:
        return

    if call.data == "add":
        msg = bot.send_message(call.message.chat.id, "متن اسپم را ارسال کنید:")
        bot.register_next_step_handler(msg, add_text)

    elif call.data == "list":
        bot.send_message(
            call.message.chat.id,
            "\n".join(spam_texts) if spam_texts else "هیچ متنی ثبت نشده"
        )

    elif call.data == "remove":
        txt = "\n".join([f"{i+1}. {t}" for i, t in enumerate(spam_texts)])
        msg = bot.send_message(call.message.chat.id, txt + "\nشماره حذف:")
        bot.register_next_step_handler(msg, remove_text)

    elif call.data == "interval":
        msg = bot.send_message(call.message.chat.id, f"فاصله فعلی بین پیام‌ها: {spam_interval} ثانیه\nعدد جدید را ارسال کنید:")
        bot.register_next_step_handler(msg, set_interval)

def add_text(m):
    spam_texts.append(m.text)
    save_data()
    bot.send_message(m.chat.id, "ذخیره شد", reply_markup=admin_menu())

def remove_text(m):
    try:
        spam_texts.pop(int(m.text)-1)
        save_data()
        bot.send_message(m.chat.id, "حذف شد", reply_markup=admin_menu())
    except:
        bot.send_message(m.chat.id, "عدد غلط", reply_markup=admin_menu())

def set_interval(m):
    global spam_interval
    try:
        val = float(m.text)
        if val < 0.1:
            val = 0.1
        spam_interval = val
        save_data()
        bot.send_message(m.chat.id, f"فاصله تنظیم شد: {spam_interval} ثانیه", reply_markup=admin_menu())
    except:
        bot.send_message(m.chat.id, "عدد معتبر وارد کنید", reply_markup=admin_menu())

# ---------------- کنترل گروه ----------------
@bot.message_handler(func=lambda m: m.reply_to_message is not None)
def control(message):
    if message.from_user.id != ADMIN_ID:
        return

    chat_id = message.chat.id
    target_id = message.reply_to_message.message_id
    chat_key = str(chat_id)

    # شروع اسپم
    if message.text == "بکل پسرم":
        enemies.setdefault(chat_key, [])
        if target_id not in enemies[chat_key]:
            enemies[chat_key].append(target_id)
            save_data()
            start_spam(chat_id, target_id)

    # توقف اسپم
    elif message.text == "بسه بیناموس":
        if target_id in enemies.get(chat_key, []):
            enemies[chat_key].remove(target_id)
            save_data()

# ---------------- اجرا ----------------
if __name__ == "__main__":
    load_data()
    bot.polling(none_stop=True)