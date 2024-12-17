import logging
import os
import yaml
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
    ConversationHandler,
)

from models.inference import ModelInference
from models.generate_picture_wrapper import sd_create_from_text
 
from utils.texts import *
from utils.token import API_TOKEN

from utils.utils import Action
    

#PATH = Path('C:\Codes\AI-telegram-bot')

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
    
    async def __create_user_info(self, user) -> None:
        print(user.id)
        self.__users_files[user.id] = {}
        self.__users_files[user.id]['full_name'] = user.full_name
        self.__users_files[user.id]['conversation'] = []    
        
    async def update_conversation(self, user, updated_conversation) -> None:
        self.__users_files[user.id]['conversation'] = updated_conversation.copy()

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command from handler"""
        return ConversationHandler.END
    
    async def start_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        await update.message.reply_text(get_start_text(), reply_markup=ReplyKeyboardRemove())

    async def help_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        await update.message.reply_text(help_text)

    async def process_user_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text.lower()
        
        user = update.message.from_user
        if user.id not in self.__users_files.keys():
            await self.__create_user_info(user)

        await update.message.reply_text(generate_text)
        
        message_class = self.model_inference.inference(
            user_message,
            None,
            task_type='cls'
        )
        
        if message_class == 0: #text
            await update.message.reply_text(generate_text)
    
            response_text, new_conversation = self.model_inference.inference(
                user_message, 
                self.__users_files[user.id]['conversation'],
                task_type='generate'
            )
            await context.bot.sendMessage(
                chat_id=update.message.chat_id,
                text=response_text,
            )
            await self.update_conversation(user, new_conversation)
            
        elif message_class == 1: #image
            image_path = sd_create_from_text(user_message, user.id)
            await update.message.reply_photo(image_path)
            
        return Action.WAIT_MESSAGE
    

def start_bot(config_path) -> None:

    app = Application.builder().token(API_TOKEN).build()
    Bot = BotHandler(config_path)
    
    app.add_handler(CommandHandler('help', Bot.help_command))
    app.add_handler(CommandHandler('start', Bot.start_command))

    create_handler = ConversationHandler(
        entry_points=[
            MessageHandler(filters.TEXT, Bot.process_user_message)
        ],
        states={
            Action.WAIT_MESSAGE: [MessageHandler(filters.TEXT, Bot.process_user_message)],
        },
        fallbacks=[
            #TODO:fallbacks
        ]
    )
    app.add_handler(create_handler)
    app.run_polling()
