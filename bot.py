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
    ConversationHandler,
)
# , sd_create_from_text
from AI_Backend.Diffusers.diffuser_model import sd_create_from_picture, sd_create_from_text, sound_preproccessing
from utils.texts import *
from utils.token import API_TOKEN
PATH = Path('C:\Codes\AI-telegram-bot')


CREATING = 1

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

    async def stop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start command from handler"""
        return ConversationHandler.END

    async def create_picture(self, update: Update, contex: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(create_paths)
        return CREATING

    async def pure_text(self, update: Update, contex: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Я пока не понимаю просто текст :(")

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

    async def picture_to_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        file_name = f"{update.message.from_user.id}_{len(self.__users_files[update.message.from_user.id]['images'])}"
        self.__users_files[update.message.from_user.id]['images'].append(
            f"{file_name}.jpg")
        path = PATH / 'Data' / 'temporary_files' / f'{file_name}.jpg'

        user_picture = await context.bot.get_file(update.message.photo[-1].file_id)
        await user_picture.download_to_drive(custom_path=path)

        picture_path = PATH / 'Data' / 'generated_files'
        if not os.path.exists(picture_path):
            os.makedirs(picture_path)
        save_path = sd_create_from_picture(pic_path=path,
                                           save_path=picture_path, user_id=update.message.from_user.id)
        await context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="I get it successful! Wait pls!")
        await update.message.reply_photo(save_path)

        return CREATING

    async def text_to_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        user_text = update.message.text
        picture_path = PATH / 'Data' / 'generated_files'
        
        if not os.path.exists(picture_path):
            os.makedirs(picture_path)
        save_path = sd_create_from_text(text=user_text,
                                        save_path=picture_path, user_id=update.message.from_user.id)
        await context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Wait pls!")
        await update.message.reply_photo(save_path)

        return CREATING

    async def voice_to_picture(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

        voice_path = PATH / 'Data' / 'temporary_files' / \
            f'{update.message.from_user.id}_voice.mp3'
        file_id = update.message.voice.file_id
        user_voice = await context.bot.get_file(file_id)
        await user_voice.download_to_drive(custom_path=voice_path)
        
        picture_path = PATH / 'Data' / 'generated_files'
        if not os.path.exists(picture_path):
            os.makedirs(picture_path)
        save_path = sound_preproccessing(sound_path=voice_path,
                                         save_path=picture_path, user_id=update.message.from_user.id)
        await context.bot.sendMessage(
            chat_id=update.message.chat_id,
            text="Wait pls!")
        await update.message.reply_photo(save_path)

        return CREATING


def main() -> None:

    app = Application.builder().token(API_TOKEN).build()
    Bot = BotHandler()
    # handlers

    app.add_handler(CommandHandler('start', Bot.start_command))
    app.add_handler(CommandHandler('help', Bot.help_command))
    app.add_handler(CommandHandler('quit', Bot.end_command))

    create_handler = ConversationHandler(
        entry_points=[CommandHandler("create", Bot.create_picture)],
        states={
            CREATING: [MessageHandler(filters.TEXT, Bot.text_to_picture),
                       MessageHandler(filters.PHOTO, Bot.picture_to_picture),
                       MessageHandler(filters.VOICE, Bot.voice_to_picture)
                       ],
        },
        fallbacks=[CommandHandler('finish', Bot.stop_command)]
    )
    app.add_handler(create_handler)

    app.run_polling()


if __name__ == '__main__':
    main()
