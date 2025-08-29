# tests/test_chatbot.py
from backend.chatbot import get_chatbot_response

def test_basic_response():
    resp = get_chatbot_response("How to grow strawberries?", preferred_lang="en")
    assert resp is not None
    assert isinstance(resp, str)
    assert len(resp) > 0
