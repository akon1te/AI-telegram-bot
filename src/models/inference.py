from models.chat_model_wrapper import GenearationModelWrapper
from models.message_classifier_wrapper import BartMessageClassifier


class ModelInference:
    def __init__(self, config):
        self.config = config
        self.qwen_wrapper = GenearationModelWrapper(self.config['generation_model']) 
        self.bart_wrapper = BartMessageClassifier(self.config['classification_model'])  

    def inference(self, message, user_conversation_history, task_type):
        if task_type == 'generate':
            responce, conversation = self.qwen_wrapper(message, user_conversation_history)
            return responce, conversation
        elif task_type == 'cls':
            print("CLS TASK STARTED")
            message_class = self.bart_wrapper(message)
            return message_class

