from diffusers import DiffusionPipeline
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
        self.pipeline = StableDiffusionPipeline.from_pretrained(
            self.model_name, 
            torch_dtype=torch.float16, 
        )
        
    def __call__(self, input_message: str) -> tuple[str, list]:
        sd_pipeline = sd_pipeline.to(self.device)
        image = self.pipeline(input_message, num_inference_steps=5, height=160, width=160).images[0]
        sd_pipeline = sd_pipeline.to('cpu')
        return image
    

