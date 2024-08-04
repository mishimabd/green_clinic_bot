from telegram import Update
from telegram.ext import ContextTypes
from groq import Groq
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = Groq(api_key="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")


async def call_groq_api(message_content: str) -> str:
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Ты виртуальный ассистент в медицинской клинике Green Clinic."
                               "Ты отвечаешь только на вопросы пациентов про их состояние, и даешь им советы."
                               "Ты очень любишь их, и вежлив. Отвечай только на русском, не добавляй английских слов."
                               "Под конец говори им то что все таки лучше следует провести глубокий анализ в нашей клинике."
                               "Отвечай на вопросы, только связанные с медициной, и с здоровьями пациентов, другие вопросы не"
                               "принимай, скажи что ты не специализируешь в этом. Отвечай только на русском!"
                               "Все ответы должны быть на русском языке только! Не добавляй никакие символы!"
                               "Если пациент говорит то что его жалобы связаны с травмотологией, перенаправь их к этим специалистам"
                               "Зоргулов Галым Серикович, травматолог, принимает пациентов с понедельника по пятницу "
                               "с 15:00 до 17:00. В субботу он не работает."
                               "Усин Ерсин Нурымханбетович, также травматолог, ведет прием с понедельника по пятницу "
                               "с 15:00 до 16:00. В субботу он также не работает."
                },
                {
                    "role": "user",
                    "content": message_content
                }
            ],
            model="llama-3.1-70b-versatile"
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Error calling Groq API: {e}")
        return "Sorry, I couldn't process your request."


# Define the Telegram bot function
async def ai_assistant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    logger.info(f"Received message: {user_message}")
    ai_response = await call_groq_api(user_message)
    logger.info(f"AI response: {ai_response}")
    await update.message.reply_text(ai_response)


async def ai_assistant_respond(update: Update, context) -> None:
    under_development_message = "Приветствую вас в клинике Green Clinic! Я виртуальный ассистент, и рад ответить на ваши вопросы о вашем состоянии здоровья и дать совет.💚"
    await update.message.reply_text(under_development_message)


async def under_development(update: Update, context) -> None:
    under_development_message = "Я в разработке...🛠"
    await update.message.reply_text(under_development_message)
