import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters, CallbackContext


async def start_button(update: Update, context: CallbackContext) -> None:
    context.user_data["is_text_for_adding"] = False

    # Determine the correct chat_id and user based on the source of the update
    if update.message:
        user = update.message.from_user
        chat_id = update.message.chat_id
    else:
        user = update.callback_query.from_user
        chat_id = update.callback_query.message.chat_id

    buttons = [
        [KeyboardButton("График Работы 🕒")],
        [KeyboardButton("Виртуальный ассистент 🤖")],
        [KeyboardButton("Платная поликлиника 🏥")],
        [KeyboardButton("Контакты 📞")],
        [KeyboardButton("Где мы расположены 📍")],
        [KeyboardButton("Изменить язык 🌐")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    # Send a new message with the buttons
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"👋Добрый день, {user.first_name}! Я официальный бот медицинского центра <b>Green Clinic</b>💚. Выберите действие:",
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    # buttons = [
    #     [KeyboardButton("Жұмыс кестесі 🕒")],
    #     [KeyboardButton("Виртуалды ассистент 🤖")],
    #     [KeyboardButton("Жекеменшік поликлиника 🏥")],
    #     [KeyboardButton("Байланыс 📞")],
    #     [KeyboardButton("Орналасқан жеріміз 📍")],
    #     [KeyboardButton("Тілді өзгерту 🌐")]
    # ]
    # reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    #
    # # Send a new message with the buttons
    # await context.bot.send_message(
    #     chat_id=chat_id,
    #     text=f"👋 Сәлем, {user.first_name}! Мен <b>Green Clinic</b> медициналық орталығының ресми боты 💚. Әрекетті таңдаңыз:",
    #     reply_markup=reply_markup,
    #     parse_mode="HTML"
    # )