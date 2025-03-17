from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from pathlib import Path


processor = TrOCRProcessor.from_pretrained("./app/models/procesor")
model = VisionEncoderDecoderModel.from_pretrained("./app/models/model")


async def recognize_photo(path_to_img: str):
    image = Image.open(path_to_img).convert("RGB")
    pixel_values = processor(images=image, return_tensors="pt").pixel_values

    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text
