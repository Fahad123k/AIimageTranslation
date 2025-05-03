from dotenv import load_dotenv
import os
from openai import OpenAI
import easyocr

load_dotenv()

class Settings:
    APP_TITLE = "Multilingual OCR Translator"
    APP_VERSION = "1.0.0"
    
    # Language configuration
    LANGUAGE_GROUPS = {
        'arabic_script': ['ar', 'en', 'ur', 'fa', ],
        'indic_script': ['en', 'hi',]
    }
    
    # OpenAI configuration
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

    @classmethod
    def get_ocr_languages(cls, target_lang: str):
        """Select appropriate language group based on target"""
        target_lang = target_lang.lower()
        if target_lang in ['ar', 'ur', 'fa']:
            return cls.LANGUAGE_GROUPS['arabic_script']
        return cls.LANGUAGE_GROUPS['indic_script']

    @classmethod
    def get_openai_client(cls):
        return OpenAI(
            base_url=cls.OPENAI_BASE_URL,
            api_key=cls.OPENROUTER_API_KEY
        )
    
    @classmethod
    def get_ocr_reader(cls, target_lang: str):
        return easyocr.Reader(
            cls.get_ocr_languages(target_lang),
            gpu=False,
            model_storage_directory='./models'
        )

settings = Settings()