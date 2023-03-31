import logging
import os

from telegram import (
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    CallbackContext,
    filters,
    Application,
    CommandHandler,
    MessageHandler,
    Updater,
)

API_TOKEN = '5467893531:AAGtHVvPbMEuT6fOVUuSjZeGT7AzV8QWWes'

from Bot.texts import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class BotHandler:
    
    __users_files = {}

    def start_command(self, update: Update, context: CallbackContext) -> None:
        """Start command from handler"""

        name = update.message.from_user.first_name
        if not name:
            name = 'User'
        
        self.__users_files[update.message.from_user.id] = {}
        self.__users_files[update.message.from_user.id]['full_name'] = update.message.from_user.full_name
                
        update.message.reply_text(get_start_text(name), reply_markup=ReplyKeyboardRemove())


    def help_command(self, update: Update, _: CallbackContext) -> None:
        """Help command from handler"""

        update.message.reply_text(help_text)
        

    def end_command(self, update: Update, _: CallbackContext) -> None:
        """End command from handler"""
        
        directory = 'temporaryfiles'

        if update.message.from_user.id in self.__users_files.keys():
            for filename in self.__users_files[update.message.from_user.id]['images']:
                cur_file = os.path.join(directory, filename + '.jpg')
                os.remove(cur_file)
            del self.__users_files[update.message.from_user.id]
                
        update.message.reply_text(end_text)


    def message_processing(self, update: Update, context: CallbackContext) -> None: 
        """Poccessing of users'message from keyboard"""

        user_message = update.message.text
        
        #TODO: design and implement smart way of interacting with user

        context.bot.send_message(
            chat_id=update.message.chat_id,
            text="INSERT BOT ANSWER HERE")
            

    def  image_processing(self, update: Update, context: CallbackContext) -> None:
        """Preproccessing and downloading user's photos"""

        try:
            file_id = update.message.photo[-1]
            newFile = context.bot.getFile(file_id)
            file_name = f"{update.message.from_user.id}_{len(self.__users_files[update.message.from_user.id]['images'])}"
            
            self.__users_files[update.message.from_user.id]['images'].append(file_name)
    
            newFile.download(
                custom_path=f"temporaryfiles/{file_name}.jpg")
            
            context.bot.sendMessage(
                chat_id=update.message.chat_id, 
                text="I get it successful!")
            
        except AttributeError:
            pass
        


def main() -> None:

    app  = Application.builder().token(API_TOKEN).build()
    Bot = BotHandler()
    # handlers
    app.add_handler(CommandHandler('start', Bot.start_command))
    app.add_handler(CommandHandler('help', Bot.help_command))
    app.add_handler(CommandHandler('quit', Bot.end_command))

    app.add_handler(MessageHandler(filters.TEXT, Bot.message_processing))
    app.add_handler(MessageHandler(filters.PHOTO, Bot.image_processing))
    #dispatcher.add_error_handler()
    
    app.run_polling()


if __name__ == '__main__':
    main()
