import logging
import os

from telegram import *
from telegram.ext import *

from utils.config import API_TOKEN

from Bot.file_processor_exmpl import process_file_command, send_botfather_command
from Bot.texts import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


def start_command(update: Update, context: CallbackContext) -> None:
    """Start command from handler"""

    name = update.message.from_user.first_name
    if not name:
        name = 'User'
    update.message.reply_text(get_start_text(name), reply_markup=ReplyKeyboardRemove())


def help_command(update: Update, _: CallbackContext) -> None:
    """Help command from handler"""

    update.message.reply_text(help_text)


def message_processing(update: Update, context: CallbackContext) -> None: 
    """Poccessing of users'message from keyboard"""

    user_message = update.message.text
    
    #TODO: design and implement smart way of interacting with user
    
    context.bot.send_message(
        chat_id=update.message.chat_id,
        text="INSERT BOT ANSWER HERE")
        

def  image_processing(update: Update, context: CallbackContext) -> None:
    """Preproccessing and downloading user's photos"""

    try:
        file_id = update.message.photo[-1]
        newFile = context.bot.getFile(file_id)
        newFile.download(custom_path=f"temporaryfiles/{update.message.from_user.first_name}'s_image.jpg")
        context.bot.sendMessage(
            chat_id=update.message.chat_id, 
            text="I get it successful!")
        
    except AttributeError:
        pass


def main() -> None:

    updater = Updater(API_TOKEN)
    dispatcher: Dispatcher = updater.dispatcher

    # handlers
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(MessageHandler(Filters.text, message_processing))
    dispatcher.add_handler(MessageHandler(Filters.photo, image_processing))
    #dispatcher.add_error_handler()
    
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
