from diffusers import DiffusionPipeline
from transformers import pipeline
import torch 

from diffusers import StableDiffusionImageVariationPipeline, StableDiffusionPipeline


class ImageGenerationWrapper:
    def __init__(self, model_config):
        self.device = model_config['device']
        if self.device == 'cuda' and not torch.cuda.is_available():
            self.device = 'cpu'
        if self.device == 'mps' and not torch.backends.mps.is_available():
            self.device = 'cpu'
        print('Model inference device: ', self.device)  
         
        self.generation_config = model_config['generation_params']
        self.model_name = model_config['model_name']
        self.sd_pipeline = StableDiffusionPipeline.from_pretrained(
            self.model_name, 
            torch_dtype=torch.float16, 
        )
        
        self.translate_model_name = model_config['translate_model_name']
        self.translate_pipeline = pipeline("translation", model=self.translate_model_name)
        
        
    def __call__(self, input_message: str) -> tuple[str, list]:
        translate_input_message = self.translate_pipeline(input_message)[0]['translation_text']
        print("TRANSLATE MSG: ", translate_input_message)
        
        self.sd_pipeline = self.sd_pipeline.to(self.device)
        image = self.sd_pipeline(translate_input_message, num_inference_steps=self.generation_config['num_inference_steps']).images[0]
        self.sd_pipeline = self.sd_pipeline.to('cpu')
        return image
    

