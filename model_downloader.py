from diffusers import StableDiffusionPipeline
import torch

model_id = "SG161222/Realistic_Vision_V5.1_noVAE"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    cache_dir="./models"
)

pipe.save_pretrained("./models/realistic-vision")