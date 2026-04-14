import telebot
from telebot import types
import time
import json
import os

# --- CONFIGURATION ---
BOT_TOKEN = "8377103854:AAEAnZ8MC7L0uEkQAEPgS_XSrCiSmgeV3D8"
bot = telebot.TeleBot(BOT_TOKEN)

# Admins: Ayush aur uska dost
ADMIN_IDS = [6450490197, 8697384673] 

DB_FILE = "pfp_database.json"
upload_session = {}

# --- BUTTON STRUCTURE ---
PAGE_1 = [
    "Profile Picture V1❤️‍🔥", "Profile Picture V2❤️‍🔥", "Profile Picture V3❤️‍🔥",
    "Profile Picture V4❤️‍🔥", "Profile Picture V5❤️‍🔥", "Profile Picture V6❤️‍🔥",
    "Profile Picture V7❤️‍🔥", "Profile Picture V8❤️‍🔥", "Profile Picture V9❤️‍🔥",
    "Profile Picture V10❤️‍🔥", "Profile Picture V11❤️‍🔥", "2nd Page💞"
]

PAGE_2 = [
    "Anime Eye's ♂️", "Dog Photo's ♂️", "Cat Photo's ♂️",
    "Aesethic Photo's ♂️", "Team Photos ♂️", "3rd Page👣", "⬅️ Back"
]

PAGE_3 = [
    "Couple pfp's💞", "About Owner☁️", "Anime🌟", "Special Page🎉",
    "Pfp For Mailboxer's, Banners,etc..💎", "Drawing's V2💢", "Drawing's V1💢",
    "⬆️ Main Menu", "⬅️ Back"
]

ALL_CATS = set(PAGE_1 + PAGE_2 + PAGE_3) - {"2nd Page💞", "3rd Page👣", "⬅️ Back", "⬆️ Main Menu"}

# Database Setup
if os.path.exists(DB_FILE):
    with open(DB_FILE, "r") as f:
        PFP_DATA = json.load(f)
else:
    PFP_DATA = {cat: [] for cat in ALL_CATS}

def save_db():
    with open(DB_FILE, "w") as f:
        json.dump(PFP_DATA, f)

def get_kb(btns):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(*[types.KeyboardButton(b) for b in btns])
    return markup

# --- START COMMAND (NEW WELCOME MESSAGE) ---
@bot.message_handler(commands=['start'])
def start(message):
    new_welcome_msg = (
        "Join💗👇🏻\n\n"
        "❤️‍🔥 @arshchat ❤️‍🔥\n"
        "      @black_bulles\n\n"
        "𝐒𝐡𝐚𝐫𝐞 𝐀𝐧𝐝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐆𝐮𝐲𝐬 𝐀𝐧𝐝 𝐉𝐨𝐢𝐧 𝐎𝐮𝐫 𝐜𝐡𝐚𝐧𝐧𝐞𝐥 𝐅𝐨𝐫 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐌𝐞𝐭𝐡𝐨𝐝𝐬 𝐀𝐧𝐝 sell :)   @arshxproofs⚡️\n\n"
        "𝐈𝐭  𝐇𝐚𝐬  𝐁𝐞𝐬𝐭  𝐌𝐞𝐭𝐡𝐬,  𝐌𝐨𝐝𝐬,  𝐈𝐧𝐬𝐭𝐚  𝐓𝐫𝐢𝐜𝐤𝐬  𝐄𝐭𝐜..  &  𝐌𝐚𝐧𝐲 𝐌𝐨𝐫𝐞 𝐓𝐡𝐢𝐧𝐠𝐬..... ❤️‍🔥\n\n"
        "𝐒𝐮𝐩𝐩𝐨𝐫𝐭 𝐌𝐞 𝐆𝐮𝐲𝐬 🥺🫶🏻"
    )
    
    bot.send_message(message.chat.id, new_welcome_msg, reply_markup=get_kb(PAGE_1))

# --- NAVIGATION ---
@bot.message_handler(func=lambda m: m.text in ["2nd Page💞", "3rd Page👣", "⬅️ Back", "⬆️ Main Menu"])
def nav(message):
    if message.text == "2nd Page💞":
        bot.send_message(message.chat.id, "Opening 2nd Page...", reply_markup=get_kb(PAGE_2))
    elif message.text == "3rd Page👣":
        bot.send_message(message.chat.id, "Opening 3rd Page...", reply_markup=get_kb(PAGE_3))
    elif message.text in ["⬅️ Back", "⬆️ Main Menu"]:
        bot.send_message(message.chat.id, "Going to Main Menu...", reply_markup=get_kb(PAGE_1))

# --- ADMIN UPLOAD ---
@bot.message_handler(content_types=['photo'])
def handle_upload(message):
    if message.from_user.id in ADMIN_IDS:
        file_id = message.photo[-1].file_id
        upload_session[message.from_user.id] = file_id
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(cat, callback_data=f"s_{cat}") for cat in list(ALL_CATS)]
        markup.add(*btns)
        bot.send_message(message.chat.id, "🛠 **ADMIN: Choose Category to save:**", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data.startswith("s_"):
        cat = call.data.split("_")[1]
        file_id = upload_session.get(call.from_user.id)
        if file_id:
            PFP_DATA[cat].append(file_id)
            save_db()
            bot.edit_message_text(f"✅ Photo Saved to {cat}!", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("del_"):
        cat = call.data.split("_")[1]
        PFP_DATA[cat] = []
        save_db()
        bot.edit_message_text(f"🗑 {cat} khali ho gaya!", call.message.chat.id, call.message.message_id)

# --- DELETE COMMAND ---
@bot.message_handler(commands=['delete'])
def delete_photos(message):
    if message.from_user.id in ADMIN_IDS:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(f"Empty {cat}", callback_data=f"del_{cat}") for cat in list(ALL_CATS)[:10]]
        markup.add(*btns)
        bot.send_message(message.chat.id, "🗑 **Admin Panel: Select category to delete photos:**", reply_markup=markup)

# --- USER CLICK (ONLY PHOTOS) ---
@bot.message_handler(func=lambda m: m.text in ALL_CATS)
def handle_cat(message):
    cat = message.text
    if cat not in PFP_DATA or not PFP_DATA[cat]:
        bot.send_message(message.chat.id, f"⚠️ Category {cat} khali hai!")
        return
    for img in PFP_DATA[cat]:
        try:
            bot.send_photo(message.chat.id, img)
            time.sleep(0.3)
        except Exception: continue

print("🚀 Bot is LIVE with New Custom Welcome Message!")
bot.infinity_polling()
