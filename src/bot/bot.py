import logging
import os
import yaml
from pathlib import Path

import numpy as np

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
    ConversationHandler,
)

from src.models.inference import ModelInference
 
from src.utils.texts import *
from src.utils.token import API_TOKEN

from utils.utils import Action
    

PATH = Path('C:\Codes\AI-telegram-bot')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


class BotHandler:

    def __init__(self, config_path):
        with open(config_path, 'r') as cfg:
            self.config = yaml.load(cfg, Loader=yaml.Loader)
        self.__users_files = {}
        self.model_inference = ModelInference(config=self.config)
    
    async def create_user_info(self, user) -> None:
        self.__users_files[user.id]['full_name'] = user.full_name
        self.__users_files[user.id]['conversation'] = []
        
    async def update_conversation(self, user, updated_conversation) -> None:
        self.__users_files[user.id]['conversation'] = (updated_conversation)

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command from handler"""
        return ConversationHandler.END

    async def help_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        await update.message.reply_text(help_text)

    async def end_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """End command from handler"""

        directory = PATH / 'Data' / 'temporary_files'

        if update.message.from_user.id in self.__users_files.keys():
            for filename in self.__users_files[update.message.from_user.id]['images']:
                cur_file = os.path.join(directory, filename + '.jpg')
                os.remove(cur_file)
            del self.__users_files[update.message.from_user.id]

        await update.message.reply_text(end_text)

    async def process_user_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text.lower()
        
        user = update.message.from_user
        if user.id not in self.__users_files.keys():
            self.__create_user_info(user)
        
        response_text, new_conversation =  self.model_inference.inference(
            user_message, 
            self.__users_file['conversation'][user.id],
            task_type='generate'
        )
                
        await context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=response_text,
        )
        
        self.update_conversation(user, new_conversation)
            
        return Action.WAIT_MESSAGE
    

def main() -> None:

    app = Application.builder().token(API_TOKEN).build()
    Bot = BotHandler()
    
    app.add_handler(CommandHandler('help', Bot.help_command))
    app.add_handler(CommandHandler('quit', Bot.end_command))

    create_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT, Bot.process_user_message)
        ],
        states={
            Action.WAIT_MESSAGE: [MessageHandler(filters.TEXT, Bot.process_user_message)]
        },
        fallbacks=[
            #TODO:fallbacks
        ]
    )
    app.add_handler(create_handler)
    app.run_polling()


if __name__ == '__main__':
    main()
