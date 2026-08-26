import os
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ستا د ټوکن له Render څخه راځي
TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ["@Sherona2", "@Rachel3427"]

# فیک ویب سرور د Render Free لپاره
web_app = Flask(__name__)
@web_app.route('/')
def home():
    return "Bot is Alive! Sherona Bot"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

# بوټ لوژیک
async def is_joined(user_id, context):
    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in ['left', 'kicked']:
                return False
        except:
            return False
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_joined(user_id, context):
        await update.message.reply_text("سلام جانک! 😍 بوټ ته ښه راغلې، اوس فعال دی!")
    else:
        keyboard = []
        for ch in CHANNELS:
            keyboard.append([InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch.replace('@','')}")])
        keyboard.append([InlineKeyboardButton("✅ Check شوم", callback_data="check")])
        await update.message.reply_text(
            "جانک لومړی په دې چینلونو کې Join شه 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def check_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if await is_joined(user_id, context):
        await query.edit_message_text("آفرین جانک! ✅ اوس بوټ فعال شو!")
    else:
        await query.answer("لا هم Join نه یې شوی جانک!", show_alert=True)

def main():
    # ویب سرور په بل تریډ کې چالان کړه
    threading.Thread(target=run_web).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(check_button, pattern="check"))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
