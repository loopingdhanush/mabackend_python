from diffusers import StableDiffusionPipeline

pipe = StableDiffusionPipeline.from_pretrained(
    "SG161222/Realistic_Vision_V5.1_noVAE",
    cache_dir="./models"
)

pipe.save_pretrained("./models/realistic-vision")

print("Model prepared successfully")