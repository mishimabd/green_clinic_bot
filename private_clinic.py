from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext


async def private_clinic_button(update: Update, context: CallbackContext) -> None:
    buttons = [
        [KeyboardButton("Отделение лучевой диагностики 🩻")],
        [KeyboardButton("Популярные направления 💡")],
        [KeyboardButton("Направления 🗺️")],
        [KeyboardButton("CHECK UP 🔍")],
        [KeyboardButton("Запись к специалисту 🩺")],
        [KeyboardButton("Назад в меню")]
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Это место, где качество обслуживания переплетается с комфортом и безопасностью, чтобы каждый человек "
        "чувствовал себя особенным и уверенным в своем здоровье.💚\n\n"
        "Выберите, что вам интересно:",
        reply_markup=reply_markup
    )


async def diagnostic_radiology_button(update: Update, context: CallbackContext) -> None:
    buttons = [
        [KeyboardButton("Магнитно-резонансная томография")],
        [KeyboardButton("Компьютерная томография")],
        [KeyboardButton("Рентген")],
        [KeyboardButton("Назад в меню")],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text(
        "Выберите, что вам интересно 💚:",
        reply_markup=reply_markup
    )


async def check_up_button(update: Update, context: CallbackContext) -> None:
    buttons = [
        [InlineKeyboardButton("Для мужчин", callback_data='for_men')],
        [InlineKeyboardButton("Для женщин", callback_data='for_women')],
        [InlineKeyboardButton("Для детей", callback_data='for_children')],
        [InlineKeyboardButton("Назад в меню", callback_data='back_to_menu')],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        "Проверь свое здоровье сегодня - будь здоров завтра!\n\n"
        "<b>💚 Профилактика</b>\n"
        " На чекап выявляются предвестники заболеваний и по результатам Вы сможете "
        "откорректировать свое здоровье, не прибегая к помощи лекарств.\n\n"
        "<b>💚 Экономия времени</b>\n"
        " Важно вовремя выявить заболевание и как можно раньше начать его лечить.\n\n"
        "<b>💚 Финансовая выгода</b>\n"
        " Затраты на Чекап сегодня — это инвестиция в Ваше будущее здоровье!\n\n"
        "Выберите, что вам интересно:",
        reply_markup=reply_markup, parse_mode="HTML"
    )


async def mri_contraindications(update: Update, context: CallbackContext) -> None:
    mri_info = (
        "<b>💚 Противопоказания</b>\n"
        "Если в теле есть металлические предметы или устройства с металлом, они будут притягиваться к магнитам, что не безопасно. "
        "Допустимы для МРТ исследований пациенты с:\n"
        "▫️ титановыми имплантами\n"
        "▫️ брекетами\n"
        "▫️ протезами суставов\n"
        "▫️ титановыми скобами на позвоночнике\n\n"
        "Это могут быть:\n\n"
        "<b>💚 Абсолютные</b>\n"
        "▫️ металлические протезы\n"
        "▫️ кардиостимуляторы\n"
        "▫️ дефибрилляторы\n"
        "▫️ нейростимуляторы\n"
        "▫️ хирургические импланты (клипсы, суставы и др.)\n"
        "▫️ помпы для доставки лекарств\n"
        "▫️ кохлеарные имплантаты\n"
        "▫️ пули или другие металлические инородные тела, попавшие в организм при несчастных случаях\n"
        "▫️ беременность 1 триместр\n\n"
        "<b>💚 Относительные</b>\n"
        "▫️ клаустрофобия\n"
        "▫️ нет возможности лежать неподвижно\n"
        "▫️ дефибрилляторы\n\n"
        "Противопоказания не являются абсолютными, каждый случай необходимо обсуждать индивидуально с врачом. "
        "То же касается беременности: в общем процедура не рекомендована, но в некоторых случаях польза превышает риск.\n\n"
        "<b>💚 Когда применяется</b>\n"
        "Магнитно-резонансная томография чаще других методов применяется для выявления заболеваний и травм мягких тканей."
    )
    image_path_or_url = 'images/important_mri.jpeg'  # Or use a URL if the image is hosted online

    # Create the inline button
    keyboard = [
        [InlineKeyboardButton("Далее", callback_data='appointment_mri')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline button
    await update.message.reply_text(mri_info, parse_mode="HTML", reply_markup=reply_markup)
    await update.message.reply_photo(photo=image_path_or_url)


async def ct_contraindications(update: Update, context: CallbackContext) -> None:
    ct_info = (
        "<b>💚 Противопоказания для компьютерной томографии</b>\n"
        "При исследованиях без контраста:\n"
        "▫️ беременность\n\n"
        "При исследованиях с контрастом:\n"
        "▫️ хроническая почечная недостаточность в стадии декомпенсации\n"
        "▫️ аллергия на ЙОД\n"
        "▫️ индивидуальная непереносимость контрастного вещества\n\n"
        "Исследование не может быть проведено пациентам, страдающим высокими степенями ожирения (вес более 100 кг)."
    )
    image_path_or_url = 'images/ct_important.jpeg'  # Or use a URL if the image is hosted online

    # Create the inline button
    keyboard = [
        [InlineKeyboardButton("Далее", callback_data='appointment_mri')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline button
    await update.message.reply_text(ct_info, parse_mode="HTML", reply_markup=reply_markup)
    await update.message.reply_photo(photo=image_path_or_url)


async def xray_contraindications(update: Update, context: CallbackContext) -> None:
    ct_info = (
        "<b>💚 Противопоказания</b>\n"
        "▫️ период беременности\n\n"
        "<b>💚 Когда применяется</b>\n"
        "Рентгенологические обследования являются одними из наиболее распространенных в современной медицине. "
        "Рентгеновское излучение используется для получения простых рентгеновских снимков костей и внутренних органов, флюорографии, "
        "в компьютерной томографии, в ангиографии и пр."
    )
    image_path_or_url = 'images/xray_important.jpeg'  # Or use a URL if the image is hosted online

    # Create the inline button
    keyboard = [
        [InlineKeyboardButton("Далее", callback_data='appointment_xray')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send the message with the inline button
    await update.message.reply_text(ct_info, parse_mode="HTML", reply_markup=reply_markup)
    await update.message.reply_photo(photo=image_path_or_url)


async def popular_service(update: Update, context: CallbackContext) -> None:
    under_development_message = "Выбери услугу которая вас интересует ниже 💚"

    keyboard = [
        [InlineKeyboardButton("Урология", callback_data='urology')],
        [InlineKeyboardButton("Общая Хирургия", callback_data='general_surgery')],
        [InlineKeyboardButton("Гастроэнтерология", callback_data='gastroenterology')],
        [InlineKeyboardButton("Педиатрия", callback_data='pediatrics')]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(under_development_message, reply_markup=reply_markup)


async def button_click_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    callback_data = query.data

    if callback_data == 'urology':
        new_text = (
            "<b>💚 О направлении</b>\n\n"
            "Урология – диагностика, лечение и профилактика заболеваний мочевой системы.\n\n"
            "<b>💚 Обязательные документы</b>\n"
            "Удостоверение личности/паспорт\n"
            "График приема специалистов\n\n"
            "<b>Леонтьев Андриан Олегович</b>\n"
            "<i>Уролог</i>\n"
            "Дата приема\n"
            "ПН 17:00-20:00\n"
            "ВТ -:-\n"
            "СР 17:00-20:00\n"
            "ЧТ -:-\n"
            "ПТ 17:00-20:00\n"
            "СБ -:-\n\n"
            "<b>Нурпеисов Ерлан Иманмагзамович</b>\n"
            "<i>Уролог</i>\н"
            "Дата приема\n"
            "ПН 9:00-13:00\n"
            "ВТ 9:00-13:00\n"
            "СР 9:00-13:00\n"
            "ЧТ 9:00-13:00\n"
            "ПТ 9:00-13:00\n"
            "СБ -:-"
        )
    elif callback_data == 'general_surgery':
        new_text = (
            "<b>💚 О направлении</b>\n\n"
            "Занимается оперативным лечением органов брюшной полости: желчный пузырь, желудок, кишечник, печень, пищевод и прочее. Также общая хирургия специализируется на лечении заболеваний кожи, мягких тканей, молочной железы и других частей тела.\n\n"
            "<b>💚 Обязательные документы</b>\n"
            "Удостоверение личности/паспорт\n"
            "График приема специалистов\n\n"
            "<b>Каиргалиев Ильяс Темиргалиевич</b>\n"
            "<i>Хирург</i>\n"
            "Дата приема\n"
            "ПН 8:00-12:00\n"
            "ВТ 8:00-12:00\n"
            "СР 8:00-12:00\n"
            "ЧТ 8:00-12:00\n"
            "ПТ 8:00-12:00\n"
            "СБ -:-"
        )
    elif callback_data == 'radiology_department':
        new_text = "You selected: Отделение лучевой диагностики"
    elif callback_data == 'gastroenterology':
        new_text = (
            "<b>💚 О направлении</b>\n\n"
            "Профилактика, диагностика и лечение заболеваний желудочно-кишечного тракта или сокращенно — ЖКТ.\n\n"
            "<b>💚 Обязательные документы</b>\n"
            "Удостоверение личности/паспорт\n"
            "График врачей\n\n"
            "<b>Ахмеджанова Лариса Рафиковна</b>\n"
            "<i>Гастроэнтеролог</i>\n"
            "Дата приема\n"
            "ПН 10:00-15:00\n"
            "ВТ 10:00-15:00\n"
            "СР 10:00-15:00\n"
            "ЧТ 10:00-15:00\n"
            "ПТ 10:00-15:00\n"
            "СБ -:-\n\n"
            "<b>Рахметова Венера Саметовна</b>\n"
            "<i>Гастроэнтеролог</i>\n"
            "Дата приема\n"
            "ПН -:-\n"
            "ВТ -:-\n"
            "СР -:-\n"
            "ЧТ -:-\n"
            "ПТ -:-\n"
            "СБ -:-\n\n"
            "<b>Конысбекова Алия Анапьяровна</b>\n"
            "<i>Гастроэнтеролог</i>\n"
            "Дата приема\n"
            "ПН 10:00-13:30\n"
            "ВТ 14:00-16:40\n"
            "СР 14:00-16:40\n"
            "ЧТ 14:00-16:40\n"
            "ПТ -:-\n"
            "СБ -:-"
        )
    elif callback_data == 'pediatrics':
        new_text = ("<b>💚 О направлении</b>\n\n"
                    "Профилактика, диагностика и лечение заболеваний детей до 18 лет.\n\n"
                    "<b>💚 Обязательные документы</b>\n"
                    "Удостоверение личности/паспорт\n"
                    "График приема специалистов\n\n"
                    "<b>Жобалаева Асем Табысовна</b>\n"
                    "<i>Педиатр</i>\n"
                    "Дата приема\n"
                    "ПН 13:00-17:00\n"
                    "ВТ 9:00-13:00\n"
                    "СР 9:00-13:00\n"
                    "ЧТ 9:00-13:00\n"
                    "ПТ 13:00-17:00\n"
                    "СБ -:-\n\n"
                    "<b>Балгабекова Жанар Биржановна</b>\n"
                    "<i>Педиатр</i>\n"
                    "Дата приема\n"
                    "ПН 9:00-13:00\n"
                    "ВТ 15:00-18:00\n"
                    "СР 9:00-13:00\n"
                    "ЧТ 15:00-18:00\n"
                    "ПТ 9:00-13:00\n"
                    "СБ 9:00-14:00")
    elif callback_data == 'appointment':
        await query.message.reply_text("Я в разработке...🛠")
        return
    elif callback_data == 'appointment_mri':
        new_text = (
            "<b>💚 Длительность</b>\n"
            "Обследование занимает 30–60 минут. В это время пациент лежит внутри томографа по возможности неподвижно. "
            "При необходимости можно провести седацию (наркоз).\n\n"
            "<b>💚 Запись на прием</b>\n"
            "Прием строго по записи. Пациент должен иметь при себе следующие документы: "
            "Удостоверение личности/паспорт/вид на жительство. "
            "Направление врача или письменная рекомендация врача в консультативном листе / выписку из амбулаторной карты (при наличии)."
        )
    elif callback_data == 'appointment_ct':
        new_text = (
            "<b>💚 Длительность</b>\n"
            "В большинстве случаев КТ длится не больше 10-15 минут. Исследование с контрастированием требует больше "
            "времени и занимает от 30 до 40 минут."
            "В это время пациент лежит внутри томографа по возможности неподвижно. При необходимости можно провести седацию (наркоз).\n\n"
            "<b>💚 Запись на прием</b>\n"
            "Прием строго по Записи. Пациент должен иметь при себе следующие документы: Удостоверение личности/паспорт/вид на жительство. "
            "Направление врача или письменная рекомендация врача в консультативном листе/выписку из амбулаторной карты (при наличии)."
        )
    elif callback_data == 'appointment_xray':
        new_text = (
            "<b>💚 Длительность</b>\n"
            "В большинстве случаев обычная рентгенография длится не больше 10-15 минут. Исследование с контрастированием "
            "требует больше времени и"
            "занимает от 30 минут до часа. При необходимости можно провести седацию (наркоз).\n\n"
            "<b>💚 Запись на прием</b>\n"
            "Прием проводится в порядке живой очереди или по предварительной записи. Пациент должен иметь при себе следующие документы: "
            "Удостоверение личности/паспорт/вид на жительство. Направление врача или письменная рекомендация врача в консультативном листе/выписку из амбулаторной карты (при наличии)."
        )
    elif callback_data == 'for_men':
        new_text = (
            "Заботьтесь о Своем Здоровье Прямо Сейчас! Выберите Свой Идеальный Чекап Пакет!\n\n"
            "💚 Мужской Базовый 300 050 ₸\n"
            "💚 Мужской ОНКО 334 830 ₸\n"
            "💚 Сердце 149 650 ₸\n"
         )
        keyboard = [
            [InlineKeyboardButton("Записаться",
                                  url='https://docs.google.com/forms/d/1pOkDdSC6pBuLvMjqWZw6GyZ7cL3tWlnrStwFXYYwr04/viewform?edit_requested=true')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=new_text, reply_markup=reply_markup, parse_mode='HTML')
        return
    elif callback_data == 'for_children':
        new_text = (
            "Заботьтесь о Своем Здоровье Прямо Сейчас! Выберите Свой Идеальный Чекап Пакет!\n\n"
            "💚 Детский Базовый 125 490 ₸\n"
            "💚 Сердце 149 650 ₸\n"
         )
        keyboard = [
            [InlineKeyboardButton("Записаться",
                                  url='https://docs.google.com/forms/d/1pOkDdSC6pBuLvMjqWZw6GyZ7cL3tWlnrStwFXYYwr04/viewform?edit_requested=true')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=new_text, reply_markup=reply_markup, parse_mode='HTML')
        return
    elif callback_data == 'for_women':
        new_text = (
            "Заботьтесь о Своем Здоровье Прямо Сейчас! Выберите Свой Идеальный Чекап Пакет!\n\n"
            "💚 Женский Базовый 310 570 ₸\n"
            "💚 Женский ОНКО 371 950 ₸\n"
            "💚 Сердце 149 650 ₸\n"
         )
        keyboard = [
            [InlineKeyboardButton("Записаться",
                                  url='https://docs.google.com/forms/d/1pOkDdSC6pBuLvMjqWZw6GyZ7cL3tWlnrStwFXYYwr04/viewform?edit_requested=true')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=new_text, reply_markup=reply_markup, parse_mode='HTML')
        return
    keyboard = [
        [InlineKeyboardButton("Записаться", callback_data='appointment')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text=new_text, reply_markup=reply_markup, parse_mode='HTML')


specialties = [
    "Аллергология", "Гастроэнтерология", "Гепатология", "Гинекология", "Дерматология",
    "Кардиология", "Лечебный Массаж", "Неврология", "Нейрохирургия", "Общая Хирургия",
    "Отоларингология", "Офтальмология", "Маммология", "Педиатрия", "Проктология",
    "Пульмонология", "Ревматология", "Терапия", "Травматология", "УЗИ", "Урология",
    "Физиотерапия", "Флебология", "Эндокринология", "Эндоскопия", "Назад в меню"
]


# Function to generate keyboard
def generate_keyboard(buttons, columns=3):
    keyboard = []
    for i in range(0, len(buttons), columns):
        row = [KeyboardButton(buttons[j]) for j in range(i, min(i + columns, len(buttons)))]
        keyboard.append(row)
    return keyboard


async def specialties_handler(update: Update, context: CallbackContext) -> None:
    message_text = update.message.text
    if message_text == "Направления 🗺️":
        keyboard = generate_keyboard(specialties, columns=3)
        new_text = "Выберите направление:"
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(text=new_text, reply_markup=reply_markup)
    else:
        await update.message.reply_text("Unexpected message received.")


