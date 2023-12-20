import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, MessageHandler, Filters
from Package import Parsing_html, Parsing_selenium, db_work as db, Parsing_pdfs

import time


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

all_tenders = Parsing_html.main()
i = 0
j = 0


# Initial menu with keyboard
def start(update: Update, context: CallbackContext):

    buttons = [[KeyboardButton("Барлық тендерлерди көрсету"),
                KeyboardButton("Жаңа тендерлерди іздеу")],
               [KeyboardButton("Тендердағы қарсыластарды талдау")],
               [KeyboardButton("Тендер қорытындыларын көрсету")]]

    # Reply message
    update.message.reply_text(
        text="Сәлем! Сізге қалай көмектесе алам?",
        reply_markup=ReplyKeyboardMarkup(buttons)
    )


# Help command. redirect to start command
def help_command(update: Update, context: CallbackContext):

    # Reply message
    update.message.reply_text(
        text="Use /start to test this bot."
    )


# Goal: deals with keyboard buttons and random messages
# -----------------------------------------------------
# It has 4 if conditions. Each deals with specific functionality
def messageHandler(update: Update, context: CallbackContext):

    # Goal: deals with showing favourable tenders
    # -------------------------------------------
    # if this function were chosen, then it sends keyboard to start
    # callback_data is 5, it will be handled by callback query in main function
    if "Барлық тендерлерди көрсету" in update.message.text:

        keyboard = [[InlineKeyboardButton("Көру!", callback_data="5")]]

        # reply message
        update.message.reply_text(
            text="<b>Тендерлердің толық сипаты көрсетілетін болады</b>\n\n"
                 "Болашақта <b>\"Анализ\"</b> түймесі істейтін болады. Әзірше құрастырулыда\n",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

    # Goal: deals with searching new tenders
    # --------------------------------------
    # if this function were chosen, then it sends keyboard to start
    # callback_data is 0, it will be handled by callback query in main function
    elif "Жаңа тендерлерди іздеу" in update.message.text:

        keyboard = [[InlineKeyboardButton("Іздеу!", callback_data="0")]]

        # reply message
        update.message.reply_text(
            text="<b>Қазір алдыңызда тендерлер шығады.</b>\n\n"
                 "Қалаған тендерлерді <b>\"Қосу\"</b> түймесі арқылы қосыңыз.\n ",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

    # Goal: deals with analyzing competitors
    # --------------------------------------
    # if this function were chosen, then it sends a keyboard of all possible tenders to analyze
    # then takes an id of tender as a callback data
    elif "Тендердағы қарсыластарды талдау" in update.message.text:

        expired_tenders_analyze = db.retrieve_expired_to_analyze()  # take list of tenders from database

        keyboard = []  # final keyboard
        special_text = ''

        # let's construct a keyboard and displayable text
        for tender in expired_tenders_analyze:
            # tender = (id, name, end_date)
            keyboard.append([InlineKeyboardButton(f'{tender[0]}', callback_data=f'{tender[0]}')])
            special_text = special_text + f'{tender[0]} - <b>{tender[1]}</b>\n\n'

        # reply message
        update.message.reply_text(
            text=special_text,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode=ParseMode.HTML
        )

    # deals with showing the final results
    elif "Тендер қорытындыларын көрсету" in update.message.text:
        update.message.reply_text(
            text="Бұл функционал әлі құрастырылып жатыр. Әзірше басқаларын қолданай тұрыңыз. \n"
                 "Соңғы жаңарту бойынша \"Жаңа тендерлерди іздеу\" функциясы істеп тұр "
        )

    # deals with random messages
    else:
        update.message.reply_text(
            text="Мен сізбен әлі сөйлесе алмайм. Әзірше басқа функцияларды қолданай тұрыңыз. \n"
                 "Соңғы жаңарту бойынша \"Жаңа тендерлерди іздеу\" функциясы істеп тұр"
        )


# Goal: Show all new tenders from Goszakup website
# ------------------------------------------------
# It showed in the format of interactive (inline) keyboard. You showed a tender, then
# you can press buttons(forward, back) to iterate through tenders.
def show_new_tenders(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()
    global i

    # given inline keyboard
    # each button has new callbackData which will be handled here too(in different if cases)
    keyboard = [[InlineKeyboardButton("Алдыңғы тендер", callback_data="1"),
                 InlineKeyboardButton("Қосу!", callback_data="2"),
                 InlineKeyboardButton("Келесі тендер", callback_data="3")],
                [InlineKeyboardButton("Шығу", callback_data="4")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # This function were used to handle callback data [01234], where "0" was sent by messagehandler and tackled here
    if query.data == "0":
        # default case
        i = 0
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
        db.add_to_db_short([all_tenders[i]['anno'], all_tenders[i]['name'], all_tenders[i]['sum'],
                            all_tenders[i]['publish'], all_tenders[i]['date'], all_tenders[i]['status'],
                            all_tenders[i]['org_bin']])

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


        db.add_to_db_full([all_tenders[i]['anno'], gov_costumer, tech_diff, level, time_given, project_designer,
                           project_designer_date])

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


# Goal: Show all available tenders in database
#
def show_available_tenders(update: Update, context: CallbackContext):

    query = update.callback_query
    query.answer()
    global j

    # given inline keyboard
    keyboard = [[InlineKeyboardButton("Алдыңғы тендер", callback_data="6"),
                 InlineKeyboardButton("Анализ", callback_data="7"),
                 InlineKeyboardButton("Келесі тендер", callback_data="8")],
                [InlineKeyboardButton("Шығу", callback_data="9")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # each button has new callbackData which will be handled here too(in different if cases)

    # This function were used to handle callback data [01234], where "0" was sent by messagehandler and tackled here
    if len(db.show_all_tenders()) == 0:
        query.edit_message_text("Кешіріңіз, сіз ешқандай тендер қоспағансыз")
    elif query.data == "5":
        # default case
        db.show_all_tenders()
        j = 0
        print_version = f'Тендер аты: <b>{db.show_all_tenders()[j][0]} {db.show_all_tenders()[j][1]}</b>\n\n' \
                        f'Статусы: {db.show_all_tenders()[j][5]}\n' \
                        f'Суммасы: {db.show_all_tenders()[j][2]} тг\n' \
                        f'Мерзімі: {db.show_all_tenders()[j][4]}\n' \
                        f'Тех сложн: {db.show_all_tenders()[j][9]} {db.show_all_tenders()[j][8]} на ' \
                        f'{db.show_all_tenders()[j][10]} месяцев\n\n' \
                        f'Генпроектировщик: {db.show_all_tenders()[j][11]} {db.show_all_tenders()[j][12]}' \
                        f'Заказчик: {db.show_all_tenders()[j][7]}\n'
        query.edit_message_text(f'{j + 1}/{len(db.show_all_tenders())} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    elif query.data == "6":
        # "previous tender button" case
        j -= 1

        print_version = f'Тендер аты: <b>{db.show_all_tenders()[j][0]} {db.show_all_tenders()[j][1]}</b> \n\n ' \
                        f'Статусы: {db.show_all_tenders()[j][5]}\n' \
                        f'Суммасы: <b>{db.show_all_tenders()[j][2]}</b>\n' \
                        f'Мерзімі: {db.show_all_tenders()[j][4]}\n' \
                        f'Тех слож: {db.show_all_tenders()[j][9]} {db.show_all_tenders()[j][8]} на ' \
                        f'{db.show_all_tenders()[j][10]} месяцев\n\n' \
                        f'Генпроектировщик: <b>{db.show_all_tenders()[j][11]} {db.show_all_tenders()[j][12]}</b>' \
                        f'Заказчик: {db.show_all_tenders()[j][7]}\n'
        query.edit_message_text(f'{j + 1}/{len(db.show_all_tenders())} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    elif query.data == "7":
        # "add tender button" case


        query.edit_message_text(f'Әзірше жұмыс істемейді',
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    elif query.data == "8":
        # "next tender button" case
        j += 1

        print_version = f'Тендер аты: <b>{db.show_all_tenders()[j][0]} {db.show_all_tenders()[j][1]}</b> \n\n ' \
                        f'Статусы: {db.show_all_tenders()[j][5]}\n' \
                        f'Суммасы: <b>{db.show_all_tenders()[j][2]}</b>\n' \
                        f'Мерзімі: {db.show_all_tenders()[j][4]}\n' \
                        f'Техническая сложность {db.show_all_tenders()[j][9]} {db.show_all_tenders()[j][8]} на ' \
                        f'{db.show_all_tenders()[j][10]} месяцев\n\n' \
                        f'Генпроектировщик: <b>{db.show_all_tenders()[j][11]} {db.show_all_tenders()[j][12]}</b>' \
                        f'Заказчик: {db.show_all_tenders()[j][7]}\n'
        query.edit_message_text(f'{j + 1}/{len(db.show_all_tenders())} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)
    else:
        # "quit button" case

        query.edit_message_text(text=f"Осыған бітті",
                                parse_mode=ParseMode.HTML)


# The function handles callbackQuery, which is the id of tender.
def analyze_competitors(update: Update, context: CallbackContext):
    print("Hello world")

    query = update.callback_query
    query.answer()

    tender_id = query.data

    filename = Parsing_selenium.retrieve_pv_file(tender_id)
    print(filename)
    competitors, pass_score = Parsing_pdfs.pvConverter(filename)
    print(competitors)

    reply_message = "Тендерге шыққан қарсыластар\n\n"

    for m in range(0, len(competitors)):
        reply_message += f'{m+1}. {str(competitors[m])}\n'

    query.edit_message_text(text=reply_message)


def main():
    """Run the bot."""
    # Create my telegram bot
    updater = Updater("5341121767:AAFZ7aztiNs4quG_iEUAG_SEPwVF7AWmo_Q")

    # Initial functions
    updater.dispatcher.add_handler(CommandHandler("start", start))  # Deal with /start command
    updater.dispatcher.add_handler(CommandHandler("help", help_command))  # Deal with /help command

    # Track which function were chosen by user and redirect it in "messageHandler" function
    updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

    # To work on search functionality
    # deals with callback data [01234]. it taken from message handler
    updater.dispatcher.add_handler(CallbackQueryHandler(show_new_tenders, pattern="[01234]"))
    updater.dispatcher.add_handler(CallbackQueryHandler(analyze_competitors, pattern="[0-9]{7}"))
    updater.dispatcher.add_handler(CallbackQueryHandler(show_available_tenders, pattern="[56789]"))


    # Run the bot until the user presses Ctrl-C
    # In order to stop the bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

# To-do list
#
# "Search new tenders" part
# 1) Track tenders that you added
# 2) Add button to see added tenders
# 3) Add functionality to remove tenders
# 4) list index out of range
# 5) Save all tenders in some file. The way I did is bad way

