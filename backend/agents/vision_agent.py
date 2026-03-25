import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
import re

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in response")
    return json.loads(match.group(0))

def analyze_outfit(shirt_base64, pants_base64, occasion):
    # build image context for prompt
    provided_items = []
    if shirt_base64:
        provided_items.append("Image 1 = Shirt")
    if pants_base64:
        provided_items.append(f"Image {'2' if shirt_base64 else '1'} = Pants")
    image_context = "\n".join(provided_items)

    prompt = f"""
You are a fashion analysis AI.

STRICT INSTRUCTIONS:
- ONLY describe what you SEE in the images
- DO NOT guess colors
- DO NOT assume common outfits
- Be visually accurate
- If unsure, say "unknown"

{image_context}

For EACH item provided extract:
- exact color (as seen)
- clothing type
- fit

Then determine:
- overall vibe
- suitability for occasion: {occasion}

Return ONLY valid JSON:

{{
  "shirt": {{"color": "", "style": "", "fit": ""}} or null if not provided,
  "pants": {{"color": "", "style": "", "fit": ""}} or null if not provided,
  "overall_vibe": "",
  "occasion": "{occasion}"
}}
"""

    # build contents dynamically
    contents = [prompt]

    if shirt_base64:
        contents.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": shirt_base64
            }
        })

    if pants_base64:
        contents.append({
            "inline_data": {
                "mime_type": "image/jpeg",
                "data": pants_base64
            }
        })

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    raw = response.text

    try:
        return extract_json(raw)
    except Exception as e:
        print("JSON ERROR:", e)
        return {
            "shirt": None,
            "pants": None,
            "overall_vibe": "unknown",
            "occasion": occasion
        }
