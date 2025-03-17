from transformers import VisionEncoderDecoderModel
from transformers import TrOCRProcessor
from pathlib import Path


def download_model(dir_to_save_model: Path, dir_to_save_processor: Path) -> None:
    model = VisionEncoderDecoderModel.from_pretrained(
        "microsoft/trocr-large-handwritten"
    )
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    processor.save_pretrained(dir_to_save_processor)  # "./data/models/processor"
    model.save_pretrained(dir_to_save_model)  # "./data/models/trocr-large"
