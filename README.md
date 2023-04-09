# AI-telegram-bot

## A bot that will generate an image at your request using stable-diffusion-v1.5 

Instructions for use:

1. /start

![Voice-to-photo](https://github.com/akon1te/AI-telegram-bot/examples/start_cmd.png)

2. /help - If you want to see all instructions for creating pictures

![Voice-to-photo](https://github.com/akon1te/AI-telegram-bot/examples/help_cmd.png)

3. /create - Using this command, the bot will wait for you to provide one of the input data options for generating images

![Voice-to-photo](https://github.com/akon1te/AI-telegram-bot/examples/create_cmd.png)

4. /finish - Finish creating regime

### For using bot, create file src/utils/token.py and insert row API_TOKEN = 'write your token here'

### Examples

1. Photo-to-photo

![Photo-to-photo](https://github.com/akon1te/AI-telegram-bot/examples/photo_to_photo.png)

2. Text-to-photo

![Text-to-photo](https://github.com/akon1te/AI-telegram-bot/examples/text_to_photo.png)

3. Voice-to-photo

Voice message: "rainbow behind blue cat:

![Voice-to-photo](https://github.com/akon1te/AI-telegram-bot/examples/voice_to_photo.png)

rainbow behind blue cat

### Used tools and models
 - Python Telegram Bot
 - Torch
 - Torchvision
 - Librosa

 - transformers
(https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-english)

 - diffusers
(https://huggingface.co/runwayml/stable-diffusion-v1-5, https://huggingface.co/lambdalabs/sd-image-variations-diffusers)



