from telegram import Update


async def doctor_appointment(update: Update, context) -> None:
    ai_assistant_message = "Я в разработке...🛠"
    await update.message.reply_text(ai_assistant_message)
