from transformers import AutoTokenizer, AutoModelForCausalLM


class GenearationModelWrapper:
    def __init__(self, model_config):
        self.generation_config = model_config['generation_params']
        self.model_name = model_config['model_name']
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
        self.system_prompt = model_config['system_prompt']
 

    def __call__(self, input_message: str, conversation_history: list) -> tuple[str, list]:
        new_conversation = []
        if conversation_history:
            conversation = conversation_history
            if len(conversation) > 5:
                conversation = conversation[-5:]
        else:
            conversation = [
                {"role": "system", "content": self.system_prompt},
            ]

        new_conversation = [
            {"role": "user", "content": input_message}
        ]
        
        response = self.model._generate(conversation.extend(new_conversation))
        new_conversation.append({"role": "assistant", "content": response})
        
        return response, new_conversation


    def _generate(self, conversation: list) -> str:
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
    