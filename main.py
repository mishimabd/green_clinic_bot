from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from basic_info import schedule_of_work, contact_numbers, location_of_clinic, menu
from ai_assistent import ai_assistant, under_development, ai_assistant_respond
from doctor_appointment import doctor_appointment
from buttons import start_button
from private_clinic import (private_clinic_button,
                            popular_service,
                            button_click_handler,
                            check_up_button,
                            ct_contraindications,
                            specialties_handler,
                            diagnostic_radiology_button,
                            xray_contraindications,
                            mri_contraindications)

TELEGRAM_BOT_TOKEN = "7492850291:AAGS4Py7BqNi3vcGcOePrGT3TgU3829HKf4"
def main():
    print(f"{datetime.now()} - Started")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_button))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(График Работы 🕒)$"), schedule_of_work))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Запись к специалисту 🩺)$"), doctor_appointment))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Популярные направления 💡)$"), popular_service))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Контакты 📞)$"), contact_numbers))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Платная поликлиника 🏥)$"), private_clinic_button))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Где мы расположены 📍)$"), location_of_clinic))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(CHECK UP 🔍)$"), check_up_button))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Назад в меню)$"), menu))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Запись к специалисту 🩺)$"), under_development))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Направления 🗺️)$"), specialties_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Отделение лучевой диагностики 🩻)$"), diagnostic_radiology_button))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Магнитно-резонансная томография)$"), mri_contraindications))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Компьютерная томография)$"), ct_contraindications))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Рентген)$"), xray_contraindications))

    application.add_handler(CallbackQueryHandler(button_click_handler))
    application.add_handler(CommandHandler("back", menu))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Виртуальный ассистент 🤖)$"), ai_assistant_respond))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_assistant))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
