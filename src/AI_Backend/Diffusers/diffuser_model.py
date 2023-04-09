from diffusers import StableDiffusionImageVariationPipeline, StableDiffusionPipeline
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
from PIL import Image
import librosa
import torch
from torchvision import transforms


def sd_create_from_text(text: str, save_path: str, user_id) -> str:

    sd_pipeline = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
    sd_pipeline = sd_pipeline.to("cuda")

    out = sd_pipeline(text)
    out['images'][0].save(f"{save_path}/{user_id}_result.jpg")
    return f"{save_path}/{user_id}_result.jpg"


def sound_preproccessing(sound_path: str, save_path: str, user_id) -> str:

    processor = Wav2Vec2Processor.from_pretrained(
        'jonatasgrosman/wav2vec2-large-xlsr-53-english')
    model = Wav2Vec2ForCTC.from_pretrained(
        'jonatasgrosman/wav2vec2-large-xlsr-53-english')

    speech_array, sampling_rate = librosa.load(sound_path, sr=16_000)
    inputs = processor(speech_array, sampling_rate=16_000,
                       return_tensors="pt", padding=True)

    with torch.no_grad():
        logits = model(inputs.input_values,
                       attention_mask=inputs.attention_mask).logits

    predicted_ids = torch.argmax(logits, dim=-1)
    predicted_sentences = processor.batch_decode(predicted_ids)[0]
    print("YOUR SENTENCE IS: ", predicted_sentences)
    
    return sd_create_from_text(text=predicted_sentences, save_path=save_path, user_id=user_id)


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
