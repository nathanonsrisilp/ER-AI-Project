import os
import tempfile

from openai import OpenAI
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

TOKEN = "8734515031:AAEXSjTlRxIXCe1tahC_STsuHU2sEJR2or4"

client = OpenAI()

# store user location
user_locations = {}


# ---------------- COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🚑 Report Emergency"],
        [KeyboardButton("📍 Share Location", request_location=True)],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🚨 ER-Helper System Online\n\n"
        "Send a voice note or describe the emergency.\n"
        "You may also share your location.",
        reply_markup=reply_markup,
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 Describe the emergency.\n"
        "Example: Fire, 3 injured, near Kasetsart University."
    )


async def location_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📍 Send Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "Tap below to share your location.",
        reply_markup=reply_markup,
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start\n/report\n/location\n/status\n\n"
        "You can also send a voice message."
    )


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📡 Status: Awaiting new report")


# ---------------- INPUT HANDLING ----------------

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🚑 Report Emergency":
        await report(update, context)
        return

    user_id = update.effective_user.id
    location = get_location_text(user_id)

    ai_report = get_ai_report(text, location)

    await send_report(update, ai_report, text)


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    user_locations[user_id] = (lat, lon)

    await update.message.reply_text(
        f"📍 Location saved\nLat: {lat}\nLon: {lon}"
    )


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 Processing voice input...")

    voice = update.message.voice
    tg_file = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        path = tmp.name

    try:
        await tg_file.download_to_drive(path)

        transcript = transcribe_audio(path)

        user_id = update.effective_user.id
        location = get_location_text(user_id)

        ai_report = get_ai_report(transcript, location)

        await send_report(update, ai_report, transcript)

    finally:
        if os.path.exists(path):
            os.remove(path)


# ---------------- AI ----------------

def transcribe_audio(file_path):
    with open(file_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )
    return result.text


def get_location_text(user_id):
    if user_id in user_locations:
        lat, lon = user_locations[user_id]
        return f"GPS: {lat}, {lon}"
    return "No GPS provided"


def get_ai_report(text, location):
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Extract emergency info.\n\n"
                    "Format strictly:\n"
                    "Incident Type:\n"
                    "Injured:\n"
                    "Location:\n"
                    "Severity:\n"
                    "Confidence:"
                ),
            },
            {
                "role": "user",
                "content": f"{text}\n{location}",
            },
        ],
    )

    return response.output_text.strip()


# ---------------- OUTPUT ----------------

async def send_report(update, report, transcript):
    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
            InlineKeyboardButton("✏️ Edit", callback_data="edit"),
            InlineKeyboardButton("🚑 Dispatch", callback_data="dispatch"),
        ]
    ]

    await update.message.reply_text(
        f"📄 TRANSCRIPT\n{transcript}\n\n"
        f"🚑 EMERGENCY ANALYSIS\n\n{report}\n\n"
        f"📡 STATUS: Pending Verification",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------------- BUTTONS ----------------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm":
        await query.edit_message_text(query.message.text + "\n\n✅ CONFIRMED")

    elif query.data == "edit":
        await query.edit_message_text(query.message.text + "\n\n✏️ PLEASE RE-ENTER DATA")

    elif query.data == "dispatch":
        await query.edit_message_text(query.message.text + "\n\n🚑 DISPATCH SENT")


# ---------------- MAIN ----------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("location", location_cmd))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status_cmd))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 ER System Running...")
    app.run_polling()


if __name__ == "__main__":
    main()