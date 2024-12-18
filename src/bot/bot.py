import logging
import os
import yaml
from pathlib import Path

from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    ReplyKeyboardMarkup,
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
 
from utils.texts import *
from utils.token import API_TOKEN

from utils.utils import (
    Action, 
    TASK_SWITCH_TO_IMG_KEYBOARD,
    TASK_SWITCH_TO_TEXT_KEYBOARD, 
    TASK_TYPE_KEYBOARD,
)
    
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)
logger = logging.getLogger(__name__)


task_type_markup = ReplyKeyboardMarkup(TASK_TYPE_KEYBOARD, one_time_keyboard=True)
task_switch_to_img_markup = ReplyKeyboardMarkup(TASK_SWITCH_TO_IMG_KEYBOARD, one_time_keyboard=True)
task_switch_to_text_markup = ReplyKeyboardMarkup(TASK_SWITCH_TO_TEXT_KEYBOARD, one_time_keyboard=True)


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
    
    async def start_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        user = update.message.from_user
        if user.id not in self.__users_files.keys():
            await self.__create_user_info(user)
            
        await update.message.reply_text(get_start_text(), reply_markup=task_type_markup)
        return Action.WAIT_MESSAGE

    async def help_command(self, update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        await update.message.reply_text(help_text)
        
    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command from handler"""
        return ConversationHandler.END
        
    async def text_task_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        print('SWITCHING TO TEXT TASK TYPE')
        await update.message.reply_text(task_type_choosing['text'])
        return Action.TEXT_GENERATION

    async def img_task_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        print('SWITCHING TO IMAGE TASK TYPE')
        await update.message.reply_text(task_type_choosing['img'])
        return Action.IMG_GENERATION
        
    async def switch_task_type(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Help command from handler"""
        await update.message.reply_text(switch_task_type_text, reply_markup=task_type_markup)
        return Action.WAIT_MESSAGE


    async def text_task_processing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text.lower()
        user = update.message.from_user

        await update.message.reply_text(generate_response_text)
        
        response_text, new_conversation =  self.model_inference.inference(
            user_message, 
            self.__users_files[user.id]['conversation'],
            task_type='generate_text'
        )
                
        await context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text=response_text,
            reply_markup=task_switch_to_img_markup
        )
        
        await self.update_conversation(user, new_conversation)
            
        return Action.TEXT_GENERATION
    
    async def image_task_processing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user_message = update.message.text.lower()
        user = update.message.from_user
        
        image =  self.model_inference.inference(
            user_message, 
            None,
            task_type='generate_image'
        )
        
        image_path = os.path.join(Path(__file__).parent.absolute(), 'tmp_images', f"{user.user_id}.jpg")
        image['images'][0].save(image_path)
         
        await context.bot.send_photo(
            chat_id=update.message.chat_id,
            photo=open(image_path, 'rb')
        )
            
        return Action.IMG_GENERATION
    

def start_bot(config_path) -> None:

    app = Application.builder().token(API_TOKEN).build()
    Bot = BotHandler(config_path)
    
    app.add_handler(CommandHandler('help', Bot.help_command))

    create_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", Bot.start_command)
        ],
        states={
            Action.WAIT_MESSAGE: [
                MessageHandler(
                    filters.Regex("^Режим диалога$"), 
                    Bot.text_task_type
                ),
                MessageHandler(
                    filters.Regex("^Режим генерации картинок$"), 
                    Bot.img_task_type
                ),
                MessageHandler(filters.TEXT, Bot.text_task_processing)
            ],
            
            Action.IMG_GENERATION: [
                MessageHandler(
                    filters.Regex("^Режим диалога$"),  
                    Bot.text_task_type
                ),
                MessageHandler(filters.TEXT, Bot.image_task_processing),
                CommandHandler('switch', Bot.switch_task_type),
            ],
            
            Action.TEXT_GENERATION: [
                MessageHandler(
                    filters.Regex("^Режим генерации картинок$"), 
                    Bot.img_task_type
                ),
                MessageHandler(filters.TEXT, Bot.text_task_processing),
                CommandHandler('switch', Bot.switch_task_type),
            ],
        },
        fallbacks=[
            #TODO:fallbacks
        ]
    )
    app.add_handler(create_handler)
    app.run_polling()
