from message_classifier_wrapper import MessageClassifierWrapper
from qwen_wrapper import GenearationModelWrapper


class ModelInference:
    def __init__(self, config):
        self.config = config
        #self.message_classifier_wrapper = MessageClassifierWrapper(self.config['message_classifier_path'])
        self.qwen_wrapper = GenearationModelWrapper(self.config['generation_model'])    

    def inference(self, message, user_conversation_history, task_type):
        if task_type == 'generate':
            responce, conversation = self.qwen_wrapper(message, user_conversation_history)
            return responce, conversation

 

    
