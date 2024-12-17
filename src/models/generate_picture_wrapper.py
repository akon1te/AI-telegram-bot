
from diffusers import StableDiffusionImageVariationPipeline, StableDiffusionPipeline
from PIL import Image
import torch

def sd_create_from_text(text: str, user_id) -> str:
    sd_pipeline = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    sd_pipeline = sd_pipeline.to("cuda")

    out = sd_pipeline(text)
    out['images'][0].save(f"src/tmp/{user_id}_result.jpg")
    return f"src/tmp/{user_id}_result.jpg"