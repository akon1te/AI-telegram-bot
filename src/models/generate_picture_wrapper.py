from diffusers import DiffusionPipeline

class ImageGenerationWrapper:
    def __init__(self, model_config):
        self.device = 'cpu'
        print('Model inference device: ', self.device)  
         
        self.generation_config = model_config['generation_params']
        self.model_name = model_config['model_name']
        self.pipeline = DiffusionPipeline.from_pretrained(self.model_name).to(self.device)
        

    def __call__(self, input_message: str) -> tuple[str, list]:

        image = self.pipeline(prompt, num_inference_steps=5, height=80, width=80).images[0]
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
    

