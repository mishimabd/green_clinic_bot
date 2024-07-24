from telegram import Update, Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext, Application, CommandHandler, MessageHandler, filters, \
    ConversationHandler


async def ai_assistant(update: Update, context) -> None:
    ai_assistant_message = "Я в разработке...🛠"
    await update.message.reply_text(ai_assistant_message)


async def under_development(update: Update, context) -> None:
    under_development_message = "Я в разработке...🛠"
    await update.message.reply_text(under_development_message)