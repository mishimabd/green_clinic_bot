from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import CallbackContext


async def change_language(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id

    # Define language buttons
    buttons = [
        [KeyboardButton("Русский 🇷🇺")],
        [KeyboardButton("Қазақша 🇰🇿")],
        [KeyboardButton("Назад 🔙")]  # Option to go back
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    # Send a message with language options
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Выберите язык:",
        reply_markup=reply_markup
    )