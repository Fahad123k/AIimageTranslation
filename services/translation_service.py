from config.settings import settings
import os


class TranslationService:
    def __init__(self):
        self.client = settings.get_openai_client()
        self.default_model = "meta-llama/llama-4-scout:free"
        self.default_temp = 0.3
        self.default_max_tokens = 1000

    async def translate_text(self, text, selected_language):
        """Translate text using OpenRouter"""
        prompt = f"Translate this to '{selected_language}' language. Note: only provide the translation as a single response without any explanation and without quotes:\n{text}"

        try:
            # print("selected: ",selected_language)
            # print("prompt: ", prompt)
            response =  self.client.chat.completions.create(
            model=self.default_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.default_temp,
            max_tokens=self.default_max_tokens,
            extra_headers=self._get_headers()  
        )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error in translation: {e}")
            return "Translation error occurred."

       

    def _get_headers(self):
        return {
            "HTTP-Referer": os.getenv("SITE_URL", "http://localhost:8000"),
            "X-Title": settings.APP_TITLE
        }

translation_service = TranslationService()