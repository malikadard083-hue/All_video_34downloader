import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler

TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = ["@Sherona2", "@Rachel3427"]

async def is_joined(context, user_id):
    for ch in CHANNELS:
        try:
            m = await context.bot.get_chat_member(ch, user_id)
            if m.status in ['left','kicked']: return False, ch
        except: return False, ch
    return True, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok, ch = await is_joined(context, update.effective_user.id)
    if not ok:
        kb = [[InlineKeyboardButton(f"Join {ch}", url=f"https://t.me/{ch.replace('@','')}")],
              [InlineKeyboardButton("✅ Check", callback_data="check")]]
        await update.message.reply_text(f"اول در {ch} جوین شو جانک!", reply_markup=InlineKeyboardMarkup(kb))
        return
    await update.message.reply_text("سلام جانک! لینک تیک تاک بفرست 🎥")

async def check_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    ok, ch = await is_joined(context, update.callback_query.from_user.id)
    if ok: await update.callback_query.message.edit_text("عالی! حالا لینک بفرست جانک ✅")
    else: await update.callback_query.answer(f"هنوز در {ch} جوین نشدی!", show_alert=True)

async def dl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ok, ch = await is_joined(context, update.effective_user.id)
    if not ok:
        await start(update, context)
        return
    url = update.message.text
    if "tiktok.com" not in url:
        await update.message.reply_text("لینک تیک تاک بفرست جانک!")
        return
    await update.message.reply_text("دارم دانلود میکنم جانک...⏳")
    try:
        opts = {'format':'mp4','outtmpl':'video.mp4','quiet':True}
        with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([url])
        with open("video.mp4","rb") as v:
            await context.bot.send_video(update.effective_chat.id, v, caption="بیا جانک 😍 @Sherona2")
        os.remove("video.mp4")
    except Exception as e:
        await update.message.reply_text(f"خطا: {e}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_btn))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, dl))
print("Bot Running...")
app.run_polling()
