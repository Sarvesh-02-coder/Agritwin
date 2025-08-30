from pathlib import Path
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from langdetect import detect
from deep_translator import GoogleTranslator
from difflib import SequenceMatcher

# --- Base directories ---
BASE_DIR = Path(__file__).resolve().parent  # chatbot backend folder
BACKEND_ROOT = BASE_DIR.parents[2]          # backend root folder

# --- Load centralized backend .env ---
ENV_PATH = BACKEND_ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# --- Configure Gemini API ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Load FAQs.json ---
FAQS_FILE = BASE_DIR / "faqs.json"
with open(FAQS_FILE, "r", encoding="utf-8") as f:
    FAQS = json.load(f)


# --- Utility functions ---
def detect_and_translate(text: str, target_lang: str = "en"):
    if not text.strip():
        return "", "unknown"
    try:
        detected_lang = detect(text)
    except Exception:
        detected_lang = "unknown"
    if detected_lang == target_lang or detected_lang == "unknown":
        return text, detected_lang
    try:
        translated = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)
        return translated, detected_lang
    except Exception:
        return text, detected_lang


def is_similar(a: str, b: str, threshold: float = 0.7) -> bool:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio() >= threshold


def search_faq(question: str) -> str | None:
    for faq in FAQS:
        if faq.get("question") and is_similar(faq["question"], question):
            return faq.get("answer")
    return None


def get_chatbot_response(user_input: str):
    translated_text, detected_lang = detect_and_translate(user_input, target_lang="en")

    # 1️⃣ Check FAQ first
    faq_answer = search_faq(translated_text)
    if faq_answer:
        if detected_lang != "en" and detected_lang != "unknown":
            try:
                faq_translated = GoogleTranslator(source="en", target=detected_lang).translate(faq_answer)
                return faq_translated, detected_lang
            except Exception:
                return faq_answer, detected_lang
        return faq_answer, detected_lang

    # 2️⃣ If not in FAQ, call Gemini
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(translated_text)
        answer_en = response.text.strip() if response and response.text else "⚠️ I couldn't generate an answer."
    except Exception as e:
        print(f"[Gemini Error] {e}")
        return f"⚠️ Error generating answer from AI: {str(e)}", detected_lang

    # Translate back if needed
    if detected_lang != "en" and detected_lang != "unknown":
        try:
            answer_translated = GoogleTranslator(source="en", target=detected_lang).translate(answer_en)
            return answer_translated, detected_lang
        except Exception:
            return answer_en, detected_lang

    return answer_en, detected_lang
