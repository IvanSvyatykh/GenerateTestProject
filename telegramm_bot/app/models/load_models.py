from transformers import TrOCRProcessor, VisionEncoderDecoderModel

processor = TrOCRProcessor.from_pretrained("kazars24/trocr-base-handwritten-ru")
processor.save_pretrained("./processor")
model = VisionEncoderDecoderModel.from_pretrained("kazars24/trocr-base-handwritten-ru")
model.save_pretrained("./model")
