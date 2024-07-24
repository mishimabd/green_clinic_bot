from telegram import Update, ReplyKeyboardMarkup, KeyboardButton



async def schedule_of_work(update: Update, context) -> None:
    work_schedule = (
        "🕒 <b>Режим работы:</b>\n\n"
        "<b>Пн-Пт:</b> 08:00 - 20:00\n"
        "<b>Сб:</b> 09:00 - 14:00\n"
        "<b>Вс:</b> выходной\n\n"
        "🏥 <i>Будем рады видеть вас в наше рабочее время!</i> 🌿"
    )
    await update.message.reply_text(work_schedule, parse_mode="HTML")


async def menu(update: Update, context) -> None:
    buttons = [
        [KeyboardButton("График Работы 🕒")],
        [KeyboardButton("Виртуальный ассистент 🤖")],
        [KeyboardButton("Платная поликлиника 🏥")],
        [KeyboardButton("Контакты 📞")],
        [KeyboardButton("Где мы расположены 📍")],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Вы попали обратно в меню!👋",
        reply_markup=reply_markup, parse_mode="HTML"
    )


async def contact_numbers(update: Update, context) -> None:
    work_schedule = (
        "<b>Контактная информация 📞</b>\n\n"
        "<b>Адрес:</b> г. Астана, ул. Хусейн бен Талал 25/1\n"
        "<b>Телефоны:</b>\n"
        "📞 +7 (7172) 79 77 22\n"
        "📲 +7 (7000) 211 211 (по прикреплению ПМСП)\n\n"
        "<b>Email:</b> <a href='mailto:info@greenclinic.kz'>info@greenclinic.kz</a> 💚"
    )
    await update.message.reply_text(work_schedule, parse_mode="HTML")


async def location_of_clinic(update: Update, context) -> None:
    latitude = 51.082759
    longitude = 71.407171

    # Send the location
    await context.bot.send_location(
        chat_id=update.effective_chat.id,
        latitude=latitude,
        longitude=longitude
    )
