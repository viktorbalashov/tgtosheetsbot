import json
import logging
import os
from datetime import datetime

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import gspread
from google.oauth2.service_account import Credentials

# ── Logging ────────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ─────────────────────────────────────────────────────────────────────
SPREADSHEET_ID = "1LZFW2gswOg_5MYZ8x0Csw_yr7uNF5MCdbY9cVWSKITU"
SHEET_GID      = "387896224"
SHEET_URL      = f"https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid={SHEET_GID}"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# ── Google Sheets ──────────────────────────────────────────────────────────────
def get_sheets_client() -> gspread.Client:
    """
    Authenticate via:
      1. GOOGLE_CREDENTIALS env variable (JSON string) — recommended for cloud
      2. credentials.json file in the same directory  — for local use
    """
    raw = os.environ.get("GOOGLE_CREDENTIALS")
    if raw:
        creds = Credentials.from_service_account_info(json.loads(raw), scopes=SCOPES)
    else:
        creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
    return gspread.authorize(creds)


def append_row(message_text: str, user_name: str, user_id: int) -> None:
    """Appends one row to the existing sheet."""
    gc          = get_sheets_client()
    spreadsheet = gc.open_by_key(SPREADSHEET_ID)

    # Open the exact tab by its numeric GID
    worksheet = spreadsheet.get_worksheet_by_id(int(SHEET_GID))

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    worksheet.append_row(
        [timestamp, user_id, user_name, message_text],
        value_input_option="USER_ENTERED",
    )
    logger.info("Row appended for user %s (%s)", user_name, user_id)


# ── Telegram handlers ──────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Отправь сообщение, и я добавлю его в Google Sheets!"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    text = update.message.text

    try:
        append_row(
            message_text=text,
            user_name=user.username or user.full_name,
            user_id=user.id,
        )
        await update.message.reply_text(
            f"Готово! Твоё сообщение здесь: {SHEET_URL}"
        )
    except Exception as exc:
        logger.exception("Failed to write to Google Sheets")
        await update.message.reply_text(
            f"❌ Что-то пошло не так:\n{exc}"
        )


# ── Entry point ────────────────────────────────────────────────────────────────
def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app   = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot is running…")
    app.run_polling()


if __name__ == "__main__":
    main()
