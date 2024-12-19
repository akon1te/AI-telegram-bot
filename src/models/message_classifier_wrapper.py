from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline


class BartMessageClassifier:
    
    def __init__(self, model_config):
        self.model_name = model_config['model_name']
        self.message_types = model_config['classes']
        self.pipeline = pipeline(model=self.model_name)

    def __call__(self, message):
        return self._predict(message)
    
    def _predict(self, message):
        outputs = self.pipeline(message,
            candidate_labels=self.message_types,
        )        
        print(outputs)
        message_type = outputs['labels'][0]
        message_index = self.message_types.index(message_type)
        
        return message_index
    