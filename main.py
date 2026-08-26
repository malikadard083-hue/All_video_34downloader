import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# تنظیمات
TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ["@Sherona2", "@Rachel3427"]

logging.basicConfig(level=logging.INFO)

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    for ch in CHANNELS:
        try:
            member = await context.bot.get_chat_member(ch, user_id)
            if member.status in ['left', 'kicked']:
                keyboard = [
                    [InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch.replace('@','')}")],
                    [InlineKeyboardButton("✅ Check کردم", callback_data="check")]
                ]
                await update.message.reply_text(
                    f"جانک اول باید در {ch} جوین شی! 😊",
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
                return False
        except:
            pass
    return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_join(update, context):
        return
    await update.message.reply_text("سلام جانک! لینک تیک تاک را بفرست تا دانلود کنم! 🎥")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_join(update, context):
        return
    
    url = update.message.text
    if "tiktok.com" not in url:
        await update.message.reply_text("لطفا یک لینک تیک تاک بفرست جانک!")
        return
    
    await update.message.reply_text("صبر جانک، دارم دانلود میکنم... ⏳")
    
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(id)s.%(ext)s',
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        with open(filename, 'rb') as f:
            await context.bot.send_video(chat_id=update.effective_chat.id, video=f, caption="بیا جانک، دانلود شد! 😍 @Sherona2")
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"خطا جانک: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()
