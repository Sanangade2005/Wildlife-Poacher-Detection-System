import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def ask_gpt(question: str) -> str:
    """
    This function now uses Gemini internally.
    Name kept for compatibility with app.py
    """

    if not GEMINI_API_KEY:
        raise RuntimeError("Gemini API key missing")

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(
        question,
        generation_config={
            "temperature": 0.4,
            "max_output_tokens": 512
        }
    )

    if not response or not response.text:
        raise RuntimeError("Empty response from Gemini")

    return response.text
