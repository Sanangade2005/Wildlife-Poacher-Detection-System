import base64
import requests
import json
from config import GEMINI_API_KEY, GEMINI_URL


def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def verify_with_gemini(image_path):
    img_base64 = encode_image(image_path)

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "You are an AI wildlife surveillance system used for anti-poaching.\n"
                            "Your task is to decide if the image contains a HUMAN POACHER based ONLY on visual evidence.\n\n"

                            "Definition of POACHER:\n"
                            "- A human present in a forest, jungle, wildlife reserve, or natural area\n"
                            "- AND carrying, holding, or using ANY weapon (gun, rifle, shotgun, bow, spear, knife)\n"
                            "- OR seen with a hunted or dead wild animal (carcass, animal body, animal being carried)\n\n"

                            "Definition of NOT a poacher:\n"
                            "- A human wearing an official army, military, or forest ranger uniform\n"
                            "- Uniforms are typically camouflage patterns in green, brown, grey, or olive colors\n"
                            "- Includes tactical vests, helmets, badges, or professional gear\n\n"

                            "STRICT RULES:\n"
                            "- Make a clear TRUE or FALSE decision\n"
                            "- Do NOT say you are unsure\n"
                            "- Do NOT mention legality, laws, or lack of context\n"
                            "- Do NOT explain uncertainty\n"
                            "- Base the decision ONLY on what is visible in the image\n\n"

                            "Respond ONLY in this strict JSON format (no extra text, no markdown):\n"
                            "{\n"
                            "  \"detected\": true or false,\n"
                            "  \"confidence\": number between 0 and 1,\n"
                            "  \"reason\": \"brief visual explanation\"\n"
                            "}"
                        )
                    },
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_base64
                        }
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(
            f"{GEMINI_URL}?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=20
        )
    except Exception as e:
        return {
            "detected": False,
            "confidence": 0.0,
            "reason": f"Request failed: {str(e)}"
        }

    if response.status_code != 200 or not response.text:
        return {
            "detected": False,
            "confidence": 0.0,
            "reason": f"Gemini HTTP error: {response.text}"
        }

    try:
        result = response.json()
        text = result["candidates"][0]["content"]["parts"][0]["text"]
        text = text.replace("```json", "").replace("```", "").strip()

        parsed = json.loads(text)

        return {
            "detected": bool(parsed.get("detected", False)),
            "confidence": float(parsed.get("confidence", 0.0)),
            "reason": parsed.get("reason", "")
        }

    except Exception as e:
        return {
            "detected": False,
            "confidence": 0.0,
            "reason": f"Invalid Gemini output: {str(e)}"
        }
