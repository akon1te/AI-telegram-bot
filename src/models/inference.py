from models.chat_model_wrapper import GenearationModelWrapper
from models.generate_picture_wrapper import ImageGenerationWrapper


class ModelInference:
    def __init__(self, config):
        self.config = config
        if 'generation_model' in self.config:
            self.qwen_wrapper = GenearationModelWrapper(self.config['generation_model']) 
        if 'image_model' in self.config:
            self.sd_wrapper = ImageGenerationWrapper(self.config['image_model'])  

    def inference(self, message, user_conversation_history, task_type):
        if task_type == 'generate_text':
            print("GENERATE TASK STARTED")
            responce, conversation = self.qwen_wrapper(message, user_conversation_history)
            return responce, conversation
        elif task_type == 'generate_picture':
            print("GENERATE IMAGE STARTED")
            image = self.sd_wrapper(message)
            return image

