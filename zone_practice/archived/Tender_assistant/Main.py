from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters

from Tender_assistant import z_tender_retrieval as tender_retrieve
from Tender_assistant import Parsing_selenium
from Tender_assistant import Parsing_pdfs



all_tenders = []


# Initial menu with keyboard
def start(update: Update, context: CallbackContext):

    buttons = [[KeyboardButton("Жаңа тендерлерди іздеу")]]

    # Reply message
    update.message.reply_text(
        text="Сәлем! Сізге қалай көмектесе алам?",
        reply_markup=ReplyKeyboardMarkup(buttons)
    )


# Goal: deals with keyboard buttons and random messages
# -----------------------------------------------------
# It has 4 if conditions. Each deals with specific functionality
def messageHandler(update: Update, context: CallbackContext):

    # Goal: deals with searching new tenders
    # --------------------------------------
    # if this function were chosen, then it sends keyboard to start
    # callback_data is 0, it will be handled by callback query in main function
    if "Жаңа тендерлерди іздеу" in update.message.text:

        keyboard = [[InlineKeyboardButton("Іздеу!", callback_data="0")]]

        # reply message
        update.message.reply_text(
            text="<b>Қазір алдыңызда тендерлер шығады.</b>\n\n"
                 "Қалаған тендерлерді <b>\"Қосу\"</b> түймесі арқылы қосыңыз.\n ",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )


# Goal: Show all new tenders from Goszakup website
# ------------------------------------------------
# It showed in the format of interactive (inline) keyboard. You showed a tender, then
# you can press buttons(forward, back) to iterate through tenders.
def show_new_tenders(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()
    global i
    global all_tenders

    # given inline keyboard
    # each button has new callbackData which will be handled here too(in different if cases)
    keyboard = [[InlineKeyboardButton("Алдыңғы тендер", callback_data="1"),
                 InlineKeyboardButton("Көрсету", callback_data="2"),
                 InlineKeyboardButton("Келесі тендер", callback_data="3")],
                [InlineKeyboardButton("Шығу", callback_data="4")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # This function were used to handle callback data [01234], where "0" was sent by messagehandler and tackled here
    if query.data == "0":
        # default case
        i = 0

        all_tenders = tender_retrieve.main()

        print_version = f'Тендер аты: <b>{all_tenders[0]["name"]}</b> \n\n Суммасы: {all_tenders[0]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[0]["date"]}'
        query.edit_message_text(f'{i + 1}/{len(all_tenders)} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    # "previous tender button" case
    elif query.data == "1":
        i -= 1
        if i == -1:
            i = len(all_tenders)-1

        print_version = f'Тендер аты: <b>{all_tenders[i]["name"]}</b> \n\n Суммасы: {all_tenders[i]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[i]["date"]}'
        query.edit_message_text(f'{i + 1}/{len(all_tenders)} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    elif query.data == "2":
        # "add tender button" case

        print_version = f'Тендер аты: <b>{all_tenders[i]["name"]}</b> \n\n Суммасы: {all_tenders[i]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[i]["date"]}'

        query.edit_message_text(text=f'<b>1/5 жүктелді</b>\n Аты, суммасы, мерзімі',
                                parse_mode=ParseMode.HTML)


        filename_tech_difficulty = Parsing_selenium.retrieve_technicality_file(all_tenders[i]['anno'])
        tech_diff, level = Parsing_pdfs.parsing_technicality_file(filename_tech_difficulty)
        query.edit_message_text(text=f'<b>2/5 жүктелді</b>\nТех сложность: {level} {tech_diff}',
                                parse_mode=ParseMode.HTML)

        filename_time_given = Parsing_selenium.retrieve_terms_file(all_tenders[i]['anno'])
        time_given = Parsing_pdfs.parsing_term_file(filename_time_given)
        query.edit_message_text(text=f'<b>3/5 жүктелді</b>\nСрок: {time_given}',
                                parse_mode=ParseMode.HTML)


        filename_project_designer = Parsing_selenium.retrieve_designer_file(all_tenders[i]['anno'])
        project_designer, project_designer_date = Parsing_pdfs.parsing_project_designer_file(filename_project_designer)
        query.edit_message_text(text=f'<b>4/5 жүктелді</b>\nГенпроектировщик: {project_designer} {project_designer_date}',
                                parse_mode=ParseMode.HTML)


        gov_costumer = Parsing_selenium.parsing_client_name(all_tenders[i]['anno'])
        query.edit_message_text(text=f'<b>5/5 жүктелді</b>\nЗаказчик: {gov_costumer}',
                                parse_mode=ParseMode.HTML)


        query.edit_message_text(f'{i + 1}/{len(all_tenders)} тендер. Тендер қосылды! \n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    elif query.data == "3":
        # "next tender button" case
        i += 1
        if i == len(all_tenders):
            i = 0

        print_version = f'Тендер аты: <b>{all_tenders[i]["name"]}</b> \n\n Суммасы: {all_tenders[i]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[i]["date"]}'
        query.edit_message_text(f'{i + 1}/{len(all_tenders)} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)
    else:
        # "quit button" case

        query.edit_message_text(text=f"<b>Тендерлер қосылды!</b> \n\n Қосылған тендерлерди көру үшін клавиатурада "
                                     f"\"Тендерлерді көру\" түймесін басыңыз",
                                parse_mode=ParseMode.HTML)


def main():
    """Run the bot."""
    # Create my telegram bot
    updater = Updater("5341121767:AAFZ7aztiNs4quG_iEUAG_SEPwVF7AWmo_Q")

    # Initial functions
    updater.dispatcher.add_handler(CommandHandler("start", start))  # Deal with /start command
    updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))


    updater.dispatcher.add_handler(CallbackQueryHandler(show_new_tenders, pattern="[01234]"))


    # Run the bot until the user presses Ctrl-C
    # In order to stop the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
