import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, ConversationHandler
from Package.Functionality_separately import Search_helper

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


all_tenders = Search_helper.main()
i = 0


def start(update: Update, context: CallbackContext):
    """Show new choice of buttons"""
    #query = update.callback_query
    #query.answer()

    keyboard = [[InlineKeyboardButton("Бастау!", callback_data="0")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        text="Қалаған тендерлерді \"Қосу\" түймесі арқылы қосыныз",
        reply_markup=reply_markup
    )


def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    global i

    keyboard = [[InlineKeyboardButton("Алдыңғы тендер", callback_data="1"),
                 InlineKeyboardButton("Қосу!", callback_data="2"),
                 InlineKeyboardButton("Келесі тендер", callback_data="3")],
                [InlineKeyboardButton("Шығу", callback_data="4")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query.data == "0":
        print_version = f'Тендер аты: <b>{all_tenders[0]["name"]}</b> \n\n Суммасы: {all_tenders[0]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[0]["date"]}'
        query.edit_message_text(f'{i+1}/{len(all_tenders)} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)
    elif query.data == "1":
        i -= 1

        print_version = f'Тендер аты: <b>{all_tenders[i]["name"]}</b> \n\n Суммасы: {all_tenders[i]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[i]["date"]}'
        query.edit_message_text(f'{i+1}/{len(all_tenders)} тендер\n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)

    elif query.data == "2":
        #global i
        #i += 1

        print_version = f'Тендер аты: <b>{all_tenders[i]["name"]}</b> \n\n Суммасы: {all_tenders[i]["sum"]} ' \
                        f'\n\nМерзімі: {all_tenders[i]["date"]}'
        query.edit_message_text(f'{i+1}/{len(all_tenders)} тендер. Тендер қосылды! \n\n' + print_version,
                                reply_markup=reply_markup,
                                parse_mode=ParseMode.HTML)
    elif query.data == "3":
            #global i
            i += 1

            print_version = f'Тендер аты: <b>{all_tenders[i]["name"]}</b> \n\n Суммасы: {all_tenders[i]["sum"]} ' \
                            f'\n\nМерзімі: {all_tenders[i]["date"]}'
            query.edit_message_text(f'{i+1}/{len(all_tenders)} тендер\n\n' + print_version,
                                    reply_markup=reply_markup,
                                    parse_mode=ParseMode.HTML)
    else:
        query.edit_message_text(text=f"<b>Тендерлер қосылды!</b> \n\n Қосылған тендерлерди көру үшін клавиатурада "
                                     f"\"Тендерлерді көру\" түймесін басыңыз",
                                parse_mode=ParseMode.HTML)


def help_command(update: Update, context: CallbackContext):
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main():
    updater = Updater("5341121767:AAFZ7aztiNs4quG_iEUAG_SEPwVF7AWmo_Q")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button, pattern="[01234]"))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
