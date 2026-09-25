import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from mutagen_proba import proces_song

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "HI! Im your server bot.\n"
        "Send me a song"
    )


async def message_menager(update: Update, context: ContextTypes.DEFAULT_TYPE):
    upit = update.message.text
    
    status_message = await update.message.reply_text(f"Looking for your song: *{upit}*", parse_mode='Markdown')
    
    try:
        
        mp3_path = proces_song(upit)
        
        await status_message.edit_text(f" Song is donwloaded.")
        
        # Opciono
        with open(mp3_path, 'rb') as audio_fajl:
            await update.message.reply_audio(audio=audio_fajl)
            
    except Exception as e:
        await status_message.edit_text(f"FATAL ERROR:\n`{e}`", parse_mode='Markdown')


if __name__ == '__main__':
    TOKEN = ""  #your telegram bot token
    
    app = ApplicationBuilder().token(TOKEN).build()
    

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_menager))
    
    print("Listening...")
    app.run_polling()