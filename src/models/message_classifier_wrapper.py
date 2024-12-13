from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline


class BartMessageClassifier:
    
    def __init__(self, model_config):
        self.model_name = model_config['model_name']
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.message_types = model_config['message_types']

    def __call__(self, message):
        return self._predict(message)
    
    def _predict(self, message):
        pipe = pipeline(model=self.model)
        outputs = pipe(message,
            candidate_labels=self.message_types,
        )        
        message_type = outputs['labels'][0]
        
        return message_type
    