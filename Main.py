import os
import tempfile
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNELS = ["@Sherona2", "@Rachel3427"]

async def check_join(update, context):
    user_id = update.effective_user.id
    for ch in CHANNELS:
        try:
            m = await context.bot.get_chat_member(ch, user_id)
            if m.status in ['left','kicked']:
                return False
        except:
            return False
    return True

async def start(update, context):
    if not await check_join(update, context):
        btn = [[InlineKeyboardButton("Join @Sherona2", url="https://t.me/Sherona2")],[InlineKeyboardButton("Join @Rachel3427", url="https://t.me/Rachel3427")],[InlineKeyboardButton("✅ Joined", callback_data="check")]]
        await update.message.reply_text("لومړی جوین شه!", reply_markup=InlineKeyboardMarkup(btn))
        return
    await update.message.reply_text("لینک راولیږه! پرته له واټرمارک ډانلوډ کوم ✅")

async def check_cb(update, context):
    q = update.callback_query
    await q.answer()
    if await check_join(update, context):
        await q.edit_message_text("مننه! اوس لینک راولیږه ✅")
    else:
        await q.answer("لا جوین نه یې!", show_alert=True)

async def download(update, context):
    if not await check_join(update, context):
        return await start(update, context)
    url = update.message.text
    if "http" not in url: return
    msg = await update.message.reply_text("⏳ ډانلوډ کوم...")
    try:
        with tempfile.TemporaryDirectory() as tmp:
            opts = {'outtmpl': f'{tmp}/%(title)s.%(ext)s','format':'best','quiet':True}
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file = ydl.prepare_filename(info)
            await update.message.reply_video(video=open(file,'rb'), caption="✅ @Sherona2")
            await msg.delete()
    except Exception as e:
        await msg.edit_text(f"ایرر: {e}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(check_cb, pattern="check"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))
app.run_polling()
