# app/services/translator_service.py
from deep_translator import GoogleTranslator

SUPPORTED_LANGUAGES = ["en", "hi", "mr"]  # English, Hindi, Marathi

def translate_text(text: str, target_lang: str = "en") -> str:
    """
    Translate text into the target language.
    - Default: English ("en")
    - Supports: Hindi ("hi"), Marathi ("mr")
    """
    try:
        if not text:
            return text

        if target_lang not in SUPPORTED_LANGUAGES:
            # Fallback to English if unsupported language is requested
            target_lang = "en"

        if target_lang == "en":
            return text  # No need to translate

        return GoogleTranslator(source="en", target=target_lang).translate(text)

    except Exception as e:
        # In case translation fails, return original text
        print(f"[Translation Error]: {e}")
        return text
