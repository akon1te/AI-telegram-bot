from diffusers import StableDiffusionImageVariationPipeline, StableDiffusionPipeline
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from PIL import Image
import torch
from torchvision import transforms

"""
def sound_preproccessing():

    # load model and processor
    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained(
        "openai/whisper-base")
    forced_decoder_ids = processor.get_decoder_prompt_ids(
        language="russian", task="translate")

    # load streaming dataset and read first audio sample
    input_speech = 0
    input_features = processor(
        input_speech["array"], sampling_rate=input_speech["sampling_rate"], return_tensors="pt").input_features

    # generate token ids
    predicted_ids = model.generate(
        input_features, forced_decoder_ids=forced_decoder_ids)
    # decode token ids to text
    transcription = processor.batch_decode(
        predicted_ids, skip_special_tokens=True)
"""

def sd_create_from_text(text: str, save_path: str, user_id):

    sd_pipeline = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    sd_pipeline = sd_pipeline.to("cuda")

    out = sd_pipeline(text)
    out['images'][0].save(f"{save_path}/{user_id}_result.jpg")
    return f"{save_path}/{user_id}_result.jpg"


def sd_create_from_picture(pic_path: str, save_path: str, user_id) -> str:

    sd_pipeline = StableDiffusionImageVariationPipeline.from_pretrained(
        "lambdalabs/sd-image-variations-diffusers",
        revision="v2.0",
    )
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    sd_pipeline = sd_pipeline.to(device)

    im = Image.open(pic_path)
    tform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize(
            (224, 224),
            interpolation=transforms.InterpolationMode.BICUBIC,
            antialias=False,
        ),
        transforms.Normalize(
            [0.48145466, 0.4578275, 0.40821073],
            [0.26862954, 0.26130258, 0.27577711]
        ),
    ])
    inp = tform(im).to(device).unsqueeze(0)

    out = sd_pipeline(inp, guidance_scale=3)
    out['images'][0].save(f"{save_path}/{user_id}_result.jpg")
    return f"{save_path}/{user_id}_result.jpg"
