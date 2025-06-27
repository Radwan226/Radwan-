import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 أهلاً بك في بوت الأفلام! 
اكتب /film متبوعًا باسم الفيلم للبحث عنه.")

async def film(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗️اكتب اسم الفيلم بعد الأمر /film")
        return

    query = " ".join(context.args)
    url = f"https://api.themoviedb.org/3/search/movie?query={query}&include_adult=false&language=ar&page=1"
    headers = {
        "Authorization": f"Bearer {TMDB_API_KEY}",
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if data.get("results"):
        movie = data["results"][0]
        title = movie.get("title", "بدون عنوان")
        overview = movie.get("overview", "لا يوجد وصف.")
        await update.message.reply_text(f"🎬 *{title}*

{overview}", parse_mode="Markdown")
    else:
        await update.message.reply_text("❌ لم يتم العثور على نتائج.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("film", film))
    app.run_polling()

if __name__ == "__main__":
    main()
