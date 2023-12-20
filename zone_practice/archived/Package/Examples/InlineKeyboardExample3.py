# Token
# 5341121767:AAFZ7aztiNs4quG_iEUAG_SEPwVF7AWmo_Q

#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, ConversationHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext):
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == "1":
        keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data="1"),
                InlineKeyboardButton("Option 2", callback_data="2"),
            ],
            [InlineKeyboardButton("Option 3", callback_data="3")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("You chose 1", reply_markup=reply_markup)
    elif query.data == "2":
        keyboard = [
            [
                InlineKeyboardButton("Option 1", callback_data="1"),
                InlineKeyboardButton("Option 2", callback_data="2"),
            ],
            [InlineKeyboardButton("Option 3", callback_data="3")],
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        query.edit_message_text("You chose 2", reply_markup=reply_markup)
    else:
        query.edit_message_text(text=f"Selected option: {query.data}")



def help_command(update: Update, context: CallbackContext):
    """Displays info on how to use the bot."""
    update.message.reply_text("Use /start to test this bot.")


def main():
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    updater = Updater("5341121767:AAFZ7aztiNs4quG_iEUAG_SEPwVF7AWmo_Q")

    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button, pattern="[123]"))
    updater.dispatcher.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
