import logging

from telegram import *
from telegram.ext import *

from Bot.config import API_TOKEN
from Bot.file_processor_exmpl import process_file_command, send_botfather_command
from Bot.texts import (
    command_tutorial_text,
    file_text,
    get_keyboard_text_handler,
    get_start_text,
    help_text,
    inline_text,
    keyboard_text,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def start_command(update: Update, _: CallbackContext) -> None:
    """Start command from handler"""

    name = update.message.from_user.first_name
    if not name:
        name = 'User'
    update.message.reply_text(get_start_text(name), reply_markup=ReplyKeyboardRemove())


def help_command(update: Update, _: CallbackContext) -> None:
    """Help command from handler"""

    update.message.reply_text(help_text)


def message_processing(update: Update, _: CallbackContext) -> None: 
    """Poccessing of users'message from keyboard"""

    #TODO: design and code this way of interacting with user


def main() -> None:

    updater = Updater(API_TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    # handlers
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(MessageHandler(Filters.text, message_processing))
    
    dispatcher.add_error_handler()
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
