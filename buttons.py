import requests
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes, MessageHandler, CommandHandler, filters, CallbackContext

async def advertise_buttons(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    buttons = [
        [KeyboardButton("Все объявления")],
        [KeyboardButton("Создать объявление")],
        [KeyboardButton("Создать объявления по файлу")],
        [KeyboardButton("Статистика")],
        [KeyboardButton("Обратно в главную")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        f"Привет, {user.first_name}! Здесь вы можете продвигать свои рекламы на Olx.kz. Выберите действие:",
        reply_markup=reply_markup
    )


async def secret_settings_buttons(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    buttons = [
        [KeyboardButton("Get list of my secret keys")],
        [KeyboardButton("Add secret key")],
        [KeyboardButton("Обратно в главную")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        f"{user.first_name}, это настройки секретного ключа на платформе Olx Developers. Выберите действие:",
        reply_markup=reply_markup
    )


async def start_button(update: Update, context: CallbackContext) -> None:
    context.user_data["is_text_for_adding"] = False
    user = update.message.from_user
    buttons = [
        [KeyboardButton("График Работы 🕒")],
        [KeyboardButton("Виртуальный ассистент 🤖")],
        [KeyboardButton("Платная поликлиника 🏥")],
        [KeyboardButton("Контакты 📞")],
        [KeyboardButton("Где мы расположены 📍")],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        f"👋Добрый день, {user.first_name}! Я официальный бот медицинского центра <b>Green Clinic</b>💚. Выберите действие:",
        reply_markup=reply_markup, parse_mode="HTML"
    )
