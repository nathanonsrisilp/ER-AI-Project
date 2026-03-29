import os
import re
import tempfile
import asyncio
import requests

from dotenv import load_dotenv
from openai import OpenAI
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

load_dotenv()

TELEGRAM_BOT_TOKEN = "8734515031:AAEXSjTlRxIXCe1tahC_STsuHU2sEJR2or4"
OPENAI_API_KEY = "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"
BACKEND_URL = "http://172.20.10.2:5001"

client = OpenAI(api_key=OPENAI_API_KEY)
user_locations = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Report Emergency"],
        [KeyboardButton("Share Location", request_location=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "🚑 ER-Helper Bot is ready.\n\n"
        "Use /report, send a voice note, or describe the emergency.",
        reply_markup=reply_markup
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "You are a world-class trained emergency response expert.\n"
        "Make a report on the emergency.\n"
        "Example: Fire, 3 injured, near SIIT."
    )


async def location_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Send My Location", request_location=True)]]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await update.message.reply_text(
        "Tap below to share your location.",
        reply_markup=reply_markup
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start - start bot\n"
        "/report - create emergency report\n"
        "/location - share location\n"
        "/help - instructions"
    )


async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lat = update.message.location.latitude
    lon = update.message.location.longitude

    user_locations[update.effective_user.id] = {
        "lat": lat,
        "lon": lon
    }

    await update.message.reply_text(
        f"📍 Location saved\nLatitude: {lat}\nLongitude: {lon}"
    )


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "Report Emergency":
        await report(update, context)
        return

    parsed = extract_report(text)
    gps = user_locations.get(update.effective_user.id, {})

    payload = {
        "incident_type": parsed["incident_type"],
        "injured": parsed["injured"],
        "location": parsed["location"],
        "severity": parsed["severity"],
        "confidence": parsed["confidence"],
        "transcript": text,
        "gps_lat": gps.get("lat"),
        "gps_lon": gps.get("lon"),
        "status": "pending",
        "source": "telegram_text",
    }

    save_report(payload)
    set_status("incoming")

    keyboard = [
        [
            InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
            InlineKeyboardButton("❌ Reject", callback_data="reject"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "🚨 EMERGENCY REPORT\n\n"
        f"Incident Type: {payload['incident_type']}\n"
        f"Injured: {payload['injured']}\n"
        f"Location: {payload['location']}\n"
        f"Severity: {payload['severity']}\n"
        f"Confidence: {payload['confidence']}\n\n"
        "📡 Status: Pending Operator Verification",
        reply_markup=reply_markup
    )


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎤 Voice message received. Transcribing...")

    voice = update.message.voice
    tg_file = await context.bot.get_file(voice.file_id)

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        temp_path = tmp.name

    try:
        await tg_file.download_to_drive(temp_path)
        transcript = transcribe_audio(temp_path)
        parsed = extract_report(transcript)
        gps = user_locations.get(update.effective_user.id, {})

        payload = {
            "incident_type": parsed["incident_type"],
            "injured": parsed["injured"],
            "location": parsed["location"],
            "severity": parsed["severity"],
            "confidence": parsed["confidence"],
            "transcript": transcript,
            "gps_lat": gps.get("lat"),
            "gps_lon": gps.get("lon"),
            "status": "pending",
            "source": "telegram_voice",
        }

        save_report(payload)
        set_status("incoming")

        keyboard = [
            [
                InlineKeyboardButton("✅ Confirm", callback_data="confirm"),
                InlineKeyboardButton("❌ Reject", callback_data="reject"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"📝 Transcript:\n{transcript}\n\n"
            "🚨 EMERGENCY REPORT\n\n"
            f"Incident Type: {payload['incident_type']}\n"
            f"Injured: {payload['injured']}\n"
            f"Location: {payload['location']}\n"
            f"Severity: {payload['severity']}\n"
            f"Confidence: {payload['confidence']}\n\n"
            "📡 Status: Pending Operator Verification",
            reply_markup=reply_markup
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "confirm":
        set_status("confirmed")
        await query.edit_message_text(
            query.message.text + "\n\n✅ Operator CONFIRMED this report."
        )

        await asyncio.sleep(5)
        set_status("idle")

    elif query.data == "reject":
        set_status("idle")
        await query.edit_message_text(
            query.message.text + "\n\n❌ Operator REJECTED this report."
        )


def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=audio_file
        )
    return transcript.text


def extract_report(text: str) -> dict:
    prompt = f"""
You are an emergency classification assistant.

Extract the emergency details from the following report.

Return ONLY in this exact format:
Incident Type: <type>
Injured: Known <known number> - Potential <potential number or unknown>
Location: <location or unknown>
Severity: <low/medium/high>
Confidence: <0.00-1.00>

Report:
{text}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    content = response.output_text.strip()

    return {
        "incident_type": parse_field(content, "Incident Type"),
        "injured": parse_field(content, "Injured"),
        "location": parse_field(content, "Location"),
        "severity": parse_field(content, "Severity"),
        "confidence": parse_field(content, "Confidence"),
    }


def parse_field(text: str, field_name: str) -> str:
    pattern = rf"{re.escape(field_name)}:\s*(.*)"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else "unknown"


def save_report(report: dict):
    requests.post(f"{BACKEND_URL}/api/reports", json=report, timeout=20)


def set_status(state: str):
    requests.get(f"{BACKEND_URL}/api/set-status?state={state}", timeout=10)


def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(CommandHandler("location", location_cmd))
    app.add_handler(CommandHandler("help", help_cmd))

    app.add_handler(CallbackQueryHandler(button_handler))

    app.add_handler(MessageHandler(filters.LOCATION, handle_location))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Telegram bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()