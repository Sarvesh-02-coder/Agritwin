from langdetect import detect
from deep_translator import LibreTranslator


def detect_and_translate(text: str, target_lang: str = "en"):
    """
    Detect language (Hindi, Marathi, English, etc.) and translate.
    Uses langdetect + deep-translator (LibreTranslate).
    """
    if not text.strip():
        return ("", "unknown") if target_lang == "en" else ""

    try:
        detected_lang = detect(text)
    except Exception:
        detected_lang = "unknown"

    # If already in target language or detection failed → return as is
    if detected_lang == target_lang or detected_lang == "unknown":
        return (text, detected_lang) if target_lang == "en" else text

    try:
        translator = LibreTranslator(source=detected_lang, target=target_lang)
        translated = translator.translate(text)

        if target_lang == "en":
            return translated, detected_lang
        else:
            return translated
    except Exception as e:
        print(f"[Translator Error] {e}")
        return (text, detected_lang) if target_lang == "en" else text
