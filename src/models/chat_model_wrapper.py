from transformers import AutoTokenizer, AutoModelForCausalLM
from time import time
import torch 


class GenearationModelWrapper:
    def __init__(self, model_config):
        self.device = model_config['device']
        if self.device == 'cuda' and not torch.cuda.is_available():
            self.device = 'cpu'
        if self.device == 'mps' and not torch.backends.mps.is_available():
            self.device = 'cpu'
        print('Model inference device: ', self.device)  
         
        self.generation_config = model_config['generation_params']
        self.model_name = model_config['model_name']
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name).to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        

    def __call__(self, input_message: str, conversation_history: list) -> tuple[str, list]:
        new_conversation = []
        conversation = conversation_history[-5:] if conversation_history else []

        new_conversation = [
            {"role": "user", "content": input_message}
        ]
        
        conversation.extend(new_conversation)
        response = self._generate(conversation)
        new_conversation.append({"role": "assistant", "content": response})

        print(new_conversation)
        return response, new_conversation


    def _generate(self, conversation: list) -> str:
        print(conversation)
        text = self.tokenizer.apply_chat_template(
            conversation,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=self.generation_config['max_new_tokens'],
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
    