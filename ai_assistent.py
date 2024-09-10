from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
from groq import Groq
import logging
from models import specialists

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key="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")
NAME, LAST_NAME, BIN, PHONE_NUMBER, SPECIALTY = range(5)


def generate_appointment_times():
    # Define Russian names for weekdays and months
    weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    months = ['янв.', 'фев.', 'мар.', 'апр.', 'май', 'июн.', 'июл.', 'авг.', 'сен.', 'окт.', 'ноя.', 'дек.']

    today = datetime.now()
    appointment_times = []

    for i in range(5):
        date = today + timedelta(days=i)
        weekday_name = weekdays[date.weekday()]
        month_name = months[date.month - 1]
        formatted_date = f"{weekday_name}, {date.day} {month_name}"
        appointment_times.append(formatted_date)

    return appointment_times


async def call_groq_api(messages: list) -> str:
    # System message to guide the AI's responses
    system_message = {
        "role": "system",
        "content": "Ты виртуальный ассистент в медицинской клинике Green Clinic."
                   "Ты отвечаешь только на вопросы пациентов про их состояние, и даешь им советы."
                   "Ты очень любишь их, и вежлив. Отвечай только на русском, не добавляй английских слов."
                   "Под конец говори им то что все таки лучше следует провести глубокий анализ в нашей клинике."
                   "Отвечай на вопросы, только связанные с медициной, и с здоровьями пациентов, другие вопросы не"
                   "принимай, скажи что ты не специализируешь в этом. Отвечай только на русском!"
                   "Все ответы должны быть на русском языке только! Не добавляй никакие символы!"
                   "Если человек захочет записаться к тебе через слова, скажи то что ему надо перейти к кнопке Платная клининка, и там записаться через кнопку Записаться."
                   "Ты не можешь записывать пациента через виртуального ассистента"
                   "Если пациент говорит то что его жалобы связаны с травмотологией, перенаправь их к этим специалистам"
                   "Зоргулов Галым Серикович, травматолог, принимает пациентов с понедельника по пятницу "
                   "с 15:00 до 17:00. В субботу он не работает."
                   "Усин Ерсин Нурымханбетович, также травматолог, ведет прием с понедельника по пятницу "
                   "с 15:00 до 16:00. В субботу он также не работает."
                   "Гастроэнтерология"
                   "Ахмеджанова Лариса Рафиковна принимает пациентов с понедельника по пятницу с 10:00 до 15:00."
                   "Конысбекова Алия Анапьяровна принимает в понедельник с 10:00 до 13:30, и со вторника по четверг с 14:00 до 16:40."
                   "Рахметова Венера Саметовна график еще не заполнен."
                   "Гепатология"
                   "Конысбекова Алия Анапьяровна принимает в понедельник с 10:00 до 13:30, и со вторника по четверг с 14:00 до 16:40."
                   "Рахметова Венера Саметовна график еще не заполнен."
                   "Гинекология"
                   "Стамкулова Актоты Шаймерденовна принимает с понедельника по пятницу с 08:15 до 14:15."
                   "Даулыбаева Алия Калиевна принимает с понедельника по пятницу с 15:00 до 19:00."
                   "Жантенова Сауле Каирбековна принимает с понедельника по пятницу с 15:00 до 17:00."
                   "Дерматология"
                   "Дунь Анастасия Павловна принимает в среду и пятницу с 14:00 до 17:30."
                   "Кардиология"
                   "Жакупова Маржангуль Аманжановна принимает с понедельника по пятницу с 09:00 до 17:00, обед с 13:00 до 14:00."
                   "Лепесова Гульжайна Улгайсыновна принимает с понедельника по пятницу с 09:00 до 16:00, обед с 12:30 до 13:30."
                   "Онгарбаева Айжан Еркиновна принимает с понедельника по пятницу с 13:00 до 14:00."
                   "Тургумбаева Жанатгуль Кабидуллиновна принимает с понедельника по четверг с 08:00 до 11:00."
                   "Тулегенова Гульдана Жолдыхановна принимает с понедельника по пятницу с 08:30 до 16:30."
                   "Лечебный массаж"
                   "Тенгебаева Гульнар принимает с понедельника по пятницу с 14:00 до 18:00, и в субботу с 09:00 до 14:00."
                   "Неврология"
                   "Дауылбаева Дина Ермановна принимает с понедельника по пятницу с 08:00 до 17:00, обед с 13:00 до 14:00."
                   "Джамантаева Ботагоз Даукеновна принимает в понедельник и пятницу с 16:00 до 18:00."
                   "Сагындыкова Галина принимает в понедельник, вторник и четверг с 15:00 до 18:00."
                   "Нейрохирургия"
                   "Шпеков Азат Салимович принимает в понедельник и среду с 17:00 до 19:00."
                   "Садвакасов Аскарбек Турсынбекович принимает во вторник и четверг с 17:00 до 19:00."
                   "Жарасов Алибек Маратович принимает в субботу с 09:00 до 14:00."
                   "Общая хирургия"
                   "Каиргалиев Ильяс Темиргалиевич принимает с понедельника по пятницу с 08:00 до 12:00."
                   "Отоларингология"
                   "Оразалинова Сания Утемисовна принимает с понедельника по пятницу с 09:00 до 17:00, обед с 13:00 до 14:00, и в субботу с 09:00 до 14:00."
                   "Офтальмология"
                   "Асыкбаева Адель Бахытовна принимает с понедельника по пятницу с 09:00 до 14:00, и в субботу с 10:00 до 14:00."
                   "Мукажанова Айнагуль Сериковна принимает в понедельник и пятницу с 14:00 до 17:00."
                   "Маммология"
                   "Кожиков Марат Климович принимает в понедельник и четверг с 17:00 до 19:00."
                   "Педиатрия"
                   "Жобалаева Асем Табысовна принимает в понедельник с 13:00 до 17:00, во вторник и четверг с 09:00 до 13:00, и в пятницу с 13:00 до 17:00."
                   "Балгабекова Жанар Биржановна принимает в понедельник с 09:00 до 13:00, во вторник и четверг с 15:00 до 18:00, в пятницу с 09:00 до 13:00, и в субботу с 09:00 до 14:00."
                   "Проктология"
                   "Сарсенова Роза Тулегеновна принимает в среду и пятницу с 10:00 до 14:00."
                   "Пульмонология"
                   "Ким Салтанат Сулейменовна принимает в четверг с 14:00 до 17:30."
                   "Корабельникова Янина Юрьевна принимает в понедельник и среду с 15:00 до 18:00."
                   "Латыпова Наталья Александровна принимает во вторник с 10:00 до 14:00."
                   "Мукатова Ирина Юрьевна график не заполнен."
                   "Серикова Аурини Сериковна принимает в понедельник, четверг и пятницу с 10:00 до 14:00."
                   "Ревматология"
                   "Кожабекова Асель Ерболовна принимает в понедельник и четверг с 15:00 до 18:00."
                   "Терапия"
                   "Аскарова Алтын Нугмановна принимает с понедельника по пятницу с 09:00 до 17:00, обед с 13:00 до 14:00."
                   "Жакупова Маржангуль Аманжановна принимает с понедельника по пятницу с 09:00 до 17:00, обед с 13:00 до 14:00."
                   "Сатыбекова Айман Амиржановна принимает с понедельника по пятницу с 08:00 до 16:00, обед с 13:00 до 14:00, и в субботу с 09:00 до 14:00."
                   "УЗИ"
                   "Аманбекова Ляззат Акановна принимает во вторник и четверг с 16:30 до 18:00."
                   "Бердибекова Кымбат Нурхановна принимает с понедельника по пятницу с 08:00 до 17:00, обед с 13:00 до 14:00."
                   "Дуйсенбаева Гулжан Зубиновна принимает с понедельника по пятницу с 08:00 до 12:00, и в субботу с 09:00 до 14:00."
                   "Нажмиденова Алия Балтабаевна принимает с понедельника по пятницу с 08:00 до 16:00, обед с 13:00 до 13:40."
                   "Урология"
                   "Леонтьев Андриан Олегович принимает в понедельник, среду и пятницу с 17:00 до 20:00."
                   "Нурпеисов Ерлан Иманмагзамович принимает с понедельника по пятницу с 09:00 до 13:00."
                   "Физиотерапия"
                   "Абенова Камал Галиолловна принимает с понедельника по пятницу с 10:00 до 17:00, обед с 12:30 до 13:00."
                   "Флебология"
                   "Адылханов Фархад Тасболатович принимает с понедельника по пятницу с 09:00 до 12:00."
                   "Эндокринология"
                   "Киноятова Дана Каиркельсыновна принимает в понедельник с 14:00 до 17:00, и со вторника по четверг с 10:00 до 13:00."
                   "Галиева Дарина Ерлановна график не заполнен."
                   "Эндоскопия"
                   "Ташимов Ренат Имангалиевич принимает с понедельника по пятницу с 09:00 до 17:00."
                   "Кокен Муратбек принимает с понедельника по пятницу с 08:00 до 17:00."

    }

    try:
        # Add system message at the beginning of the conversation history
        conversation_with_system_message = [system_message] + messages

        chat_completion = client.chat.completions.create(
            messages=conversation_with_system_message,
            model="llama-3.1-70b-versatile"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Groq API: {e}")
        return "Sorry, I couldn't process your request."


async def ai_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")

    # Retrieve conversation history from user_data
    if "conversation_history" not in context.user_data:
        context.user_data["conversation_history"] = []

    if user_message.lower() == "/clear":
        await clear_history(update, context)
        return

    # Append user message to conversation history
    context.user_data["conversation_history"].append({
        "role": "user",
        "content": user_message
    })

    # Get the response from the AI
    ai_response = await call_groq_api(context.user_data["conversation_history"])
    logger.info(f"AI response: {ai_response}")

    # Append AI response to conversation history
    context.user_data["conversation_history"].append({
        "role": "assistant",
        "content": ai_response
    })

    await update.message.reply_text(ai_response)


async def ai_assistant_respond(update: Update, context) -> None:
    under_development_message = "Приветствую вас в клинике Green Clinic! Я виртуальный ассистент, и рад ответить на ваши вопросы о вашем состоянии здоровья и дать совет.💚"
    await update.message.reply_text(under_development_message)


async def under_development(update: Update, context) -> None:
    under_development_message = "Я в разработке...🛠"
    await update.message.reply_text(under_development_message)


async def clear_history(update: Update, context: CallbackContext) -> None:
    context.user_data["conversation_history"] = []
    await update.message.reply_text("Запись памяти была очищена! Задавайте ваши вопросы.")


async def start_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Пожалуйста, введите ваше имя:")
    return NAME


async def handle_first_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['first_name'] = update.message.text
    await update.message.reply_text("Теперь введите вашу фамилию:")
    return LAST_NAME


async def handle_last_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['last_name'] = update.message.text
    await update.message.reply_text(
        "Теперь введите ваш ИИН. Будьте уверены, что ваш ИИН останется строго конфиденциальным."
    )
    return BIN


async def handle_bin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['bin'] = update.message.text
    await request_phone_number(update, context)
    return PHONE_NUMBER


async def request_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Отправить номер телефона", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Пожалуйста, отправьте свой номер телефона:", reply_markup=reply_markup)


async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    contact = update.message.contact
    context.user_data['phone_number'] = contact.phone_number

    # Clear the custom keyboard by sending a message without a reply_markup
    await update.message.reply_text("Спасибо! Теперь выберите специализацию.", reply_markup=ReplyKeyboardRemove())

    await display_specialties(update, context)
    return SPECIALTY


async def display_specialties(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [InlineKeyboardButton(specialty, callback_data=specialty)]
        for specialty in specialists.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выберите специализацию:", reply_markup=reply_markup)
    return ConversationHandler.END


async def display_specialists(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_specialty = query.data
    context.user_data['selected_specialty'] = selected_specialty

    keyboard = [
        [InlineKeyboardButton(specialist, callback_data=specialist)]
        for specialist in specialists[selected_specialty]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    new_text = f"Вы выбрали {selected_specialty}. Выберите специалиста:"
    await query.edit_message_text(text=new_text, reply_markup=reply_markup)


async def select_appointment_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_specialist = query.data
    context.user_data['selected_specialist'] = selected_specialist

    keyboard = [
        [InlineKeyboardButton("Консультация", callback_data="Консультация")],
        [InlineKeyboardButton("Диагностика", callback_data="Диагностика")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    new_text = f"Вы выбрали {selected_specialist}. Выберите тип посещения:"
    await query.edit_message_text(text=new_text, reply_markup=reply_markup)


async def select_appointment_time(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_type = query.data
    context.user_data['selected_type'] = selected_type

    appointment_times = generate_appointment_times()

    keyboard = [
        [InlineKeyboardButton(time, callback_data=time)]
        for time in appointment_times
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    new_text = f"Вы выбрали {selected_type}. Выберите время для записи:"
    await query.edit_message_text(text=new_text, reply_markup=reply_markup)


async def select_payment_method(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    selected_time = query.data
    context.user_data['selected_time'] = selected_time

    keyboard = [
        [InlineKeyboardButton("Клиент", callback_data="Клиент")],
        [InlineKeyboardButton("Страховая компания", callback_data="Страховая компания")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    new_text = f"Вы выбрали время {selected_time}. Кто оплачивает прием?"
    await query.edit_message_text(text=new_text, reply_markup=reply_markup)


async def confirm_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    selected_payment = query.data
    selected_specialty = context.user_data.get('selected_specialty', 'Не указан')
    selected_specialist = context.user_data.get('selected_specialist', 'Не указан')
    selected_type = context.user_data.get('selected_type', 'Не указан')
    selected_time = context.user_data.get('selected_time', 'Не указан')
    phone_number = context.user_data.get('phone_number', 'Не указан')
    first_name = context.user_data.get('first_name', 'Не указан')
    last_name = context.user_data.get('last_name', 'Не указан')
    bin = context.user_data.get('bin', 'Не указан')

    confirmation_text = (
        f"Вы выбрали:\n"
        f"Имя: {first_name}\n"
        f"Фамилия: {last_name}\n"
        f"БИН: {bin}\n"
        f"Специализация: {selected_specialty}\n"
        f"Специалист: {selected_specialist}\n"
        f"Тип посещения: {selected_type}\n"
        f"Время: {selected_time}\n"
        f"Оплачивает: {selected_payment}\n"
        f"Телефон: {phone_number}\n"
        f"Для подтверждения записи, нажмите кнопку ниже."
    )

    context.user_data['confirmation_text'] = confirmation_text

    keyboard = [
        [InlineKeyboardButton("Подтвердить запись", callback_data="confirm_appointment")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=confirmation_text, reply_markup=reply_markup)
