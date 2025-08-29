# backend/voice.py
import os
from pydub import AudioSegment
import speech_recognition as sr
from gtts import gTTS
from pathlib import Path
import uuid

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _ensure_wav(input_path: str) -> str:
    """
    Convert non-wav audio to wav using pydub (requires ffmpeg installed).
    Returns path to wav file (may be same as input if already wav).
    """
    path = Path(input_path)
    if path.suffix.lower() == ".wav":
        return input_path
    wav_path = str(path.with_suffix(".wav"))
    try:
        audio = AudioSegment.from_file(input_path)
        audio.export(wav_path, format="wav")
        return wav_path
    except Exception:
        # If conversion fails, return original path and let recognizer attempt
        return input_path

def speech_to_text(audio_file_path: str) -> tuple:
    """
    Returns (transcribed_text, detected_lang) where detected_lang is 'en'/'hi'/'mr'.
    Attempts Hindi then Marathi then English recognition via Google's STT.
    """
    wav_path = _ensure_wav(audio_file_path)
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)

    # Try Hindi
    try:
        text_hi = recognizer.recognize_google(audio_data, language="hi-IN")
        if text_hi and len(text_hi.strip()) > 0:
            return text_hi, "hi"
    except Exception:
        pass

    # Try Marathi
    try:
        text_mr = recognizer.recognize_google(audio_data, language="mr-IN")
        if text_mr and len(text_mr.strip()) > 0:
            return text_mr, "mr"
    except Exception:
        pass

    # Try English
    try:
        text_en = recognizer.recognize_google(audio_data, language="en-IN")
        if text_en and len(text_en.strip()) > 0:
            return text_en, "en"
    except Exception:
        pass

    # As a last resort try default recognizer
    try:
        text_def = recognizer.recognize_google(audio_data)
        return text_def, "en"
    except Exception:
        return "", "en"

def text_to_speech(text: str, lang: str = "en") -> str:
    """
    Convert text to speech. Saves file in data/ and returns filepath (relative to project).
    lang expected: 'en', 'hi', 'mr'
    Note: gTTS supports 'hi' and 'mr' languages in many environments.
    """
    if not text:
        text = "Sorry, I couldn't generate a voice response."

    # Map lang codes for gTTS
    lang_map = {"en": "en", "hi": "hi", "mr": "mr"}
    tts_lang = lang_map.get(lang, "en")

    file_name = f"answer_{uuid.uuid4().hex}.mp3"
    file_path = DATA_DIR / file_name

    try:
        tts = gTTS(text=text, lang=tts_lang)
        tts.save(str(file_path))
        return str(file_path.name)  # return filename only - app returns /audio/{filename}
    except Exception as e:
        # fallback: try english
        try:
            tts = gTTS(text=text, lang="en")
            tts.save(str(file_path))
            return str(file_path.name)
        except Exception:
            # if all fail, return empty
            return ""
