from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ConversationHandler, filters
from basic_info import schedule_of_work, contact_numbers, location_of_clinic, menu
from ai_assistent import ai_assistant, under_development, ai_assistant_respond, display_specialties, \
    display_specialists, select_appointment_time, confirm_appointment, generate_appointment_times, \
    select_appointment_type, select_payment_method, handle_contact, request_phone_number, \
    handle_first_name, handle_last_name, handle_bin, start_appointment
from doctor_appointment import doctor_appointment
from buttons import start_button
from language import change_language
from models import specialists
from private_clinic import (private_clinic_button,
                            popular_service,
                            button_click_handler,
                            check_up_button,
                            ct_contraindications,
                            specialties_handler,
                            diagnostic_radiology_button,
                            xray_contraindications,
                            mri_contraindications)
NAME, LAST_NAME, BIN, PHONE_NUMBER, SPECIALTY = range(5)
TELEGRAM_BOT_TOKEN = "7492850291:AAGS4Py7BqNi3vcGcOePrGT3TgU3829HKf4"
def main():
    print(f"{datetime.now()} - Started")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add ConversationHandler for the user information flow
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & filters.Regex("^(Запись к специалисту 🩺)$"), start_appointment)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_first_name)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_last_name)],
            BIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_bin)],
            PHONE_NUMBER: [MessageHandler(filters.CONTACT, handle_contact)],
        },
        fallbacks=[CommandHandler("nigga", start_appointment)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(График Работы 🕒)$"), schedule_of_work))
    application.add_handler(CallbackQueryHandler(display_specialists, pattern='|'.join(specialists.keys())))
    application.add_handler(CallbackQueryHandler(select_appointment_type, pattern='|'.join(
        [specialist for sublist in specialists.values() for specialist in sublist])))
    application.add_handler(CallbackQueryHandler(select_appointment_time, pattern='Консультация|Диагностика'))
    application.add_handler(CallbackQueryHandler(select_payment_method, pattern='|'.join(generate_appointment_times())))
    application.add_handler(CallbackQueryHandler(confirm_appointment, pattern='Клиент|Страховая компания'))

    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Поделиться номером телефона)$"), request_phone_number))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Направления 🗺️)$"), specialties_handler))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Изменить язык 🌐)$"), change_language))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Популярные направления 💡)$"), popular_service))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Контакты 📞)$"), contact_numbers))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Платная поликлиника 🏥)$"), private_clinic_button))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Где мы расположены 📍)$"), location_of_clinic))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(CHECK UP 🔍)$"), check_up_button))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Назад в меню)$"), menu))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Отделение лучевой диагностики 🩻)$"),
                                           diagnostic_radiology_button))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Магнитно-резонансная томография)$"), mri_contraindications))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Компьютерная томография)$"), ct_contraindications))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("^(Рентген)$"), xray_contraindications))

    application.add_handler(CallbackQueryHandler(button_click_handler))
    application.add_handler(CommandHandler("back", menu))
    application.add_handler(
        MessageHandler(filters.TEXT & filters.Regex("^(Виртуальный ассистент 🤖)$"), ai_assistant_respond))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, ai_assistant))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
