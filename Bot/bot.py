import logging
import os

from pathlib import Path

from telegram import (
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    ContextTypes,
    filters,
    Application,
    CommandHandler,
    MessageHandler,
    Updater,
)

PATH = Path('/mnt/d/MyCode/AI-telegram-bot')

API_TOKEN = '5467893531:AAGtHVvPbMEuT6fOVUuSjZeGT7AzV8QWWes'

from texts import *

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class BotHandler:
    
    __users_files = {}

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command from handler"""

        name = update.message.from_user.first_name
        if not name:
            name = 'User'
        
        self.__users_files[update.message.from_user.id] = {}
        self.__users_files[update.message.from_user.id]['full_name'] = update.message.from_user.full_name
        self.__users_files[update.message.from_user.id]['images'] = []
                
        await update.message.reply_text(get_start_text(name), reply_markup=ReplyKeyboardRemove())


    def help_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""

        update.message.reply_text(help_text)
        

    async def end_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """End command from handler"""
        
        directory = PATH / 'Data' / 'temporaryfiles'

        if update.message.from_user.id in self.__users_files.keys():
            for filename in self.__users_files[update.message.from_user.id]['images']:
                cur_file = os.path.join(directory, filename + '.jpg')
                os.remove(cur_file)
            del self.__users_files[update.message.from_user.id]
                
        await update.message.reply_text(end_text)


    async def message_processing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None: 
        """Poccessing of users'message from keyboard"""

        user_message = update.message.text
        
        #TODO: design and implement smart way of interacting with user

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="INSERT BOT ANSWER HERE")
            

    async def image_processing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Preproccessing and downloading user's photos"""
        
        try:
            file_name = f"{update.message.from_user.id}_{len(self.__users_files[update.message.from_user.id]['images'])}"
            self.__users_files[update.message.from_user.id]['images'].append(file_name)
            path = PATH / 'Data' / 'temporaryfiles' / f'{file_name}.jpg'
            
            file_id = update.message.photo[-1].file_id
            new_file = await context.bot.get_file(file_id)
            await new_file.download_to_drive(custom_path=path)
            
            await context.bot.sendMessage(
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
