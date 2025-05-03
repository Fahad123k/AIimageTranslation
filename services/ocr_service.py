from PIL import Image, ImageOps, ImageEnhance
import numpy as np
from config.settings import settings

class OCRService:
    def __init__(self, target_lang: str):
        self.target_lang = target_lang
        self.reader = settings.get_ocr_reader(target_lang)

    async def process_image(self, image_bytes):
        """Process image and perform OCR"""
        image = Image.open(image_bytes)
        image = self._preprocess_image(image)
        image_np = np.array(image)
        return self._perform_ocr(image_np)

    def _preprocess_image(self, image):
        """Image preprocessing pipeline"""
        image = ImageOps.exif_transpose(image)
        image = image.convert('L')
        image.thumbnail((1600, 1600))
        image = ImageEnhance.Contrast(image).enhance(2.0)
        return image.point(lambda x: 0 if x < 140 else 255)

    def _perform_ocr(self, image_np):
        """Perform OCR on processed image"""
        results = self.reader.readtext(image_np, detail=0)
        return " ".join(results)


OCRService=OCRService(target_lang="en")  # Default to English, can be changed as needed