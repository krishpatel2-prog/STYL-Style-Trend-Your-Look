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

def analyze_outfit(shirt_base64, pants_base64, occasion, gender="neutral"):
    # build image context for prompt
    provided_items = []
    if shirt_base64:
        provided_items.append("Image 1 = Shirt")
    if pants_base64:
        provided_items.append(f"Image {'2' if shirt_base64 else '1'} = Pants")
    image_context = "\n".join(provided_items)

    prompt = f"""
    You are a brutally honest but friendly AI fashion stylist — like a knowledgeable best friend who tells you the truth.

    {image_context}
    Occasion: {occasion}
    Gender: {gender}

    Analyze the uploaded clothing items visually.

    Then give:
    1. Raw visual data (color, style, fit) for each item
    2. An honest stylist verdict — does this actually work for {occasion}? Be real, add personality. Use fashion terms. If it doesn't work for the occasion say so directly but constructively.
    3. A vibe label with emoji (e.g. "Sleek & Mysterious 🖤", "Wedding Ready ✨", "Too Casual for This 😬")
    4. Occasion match score out of 10

    OCCASION INTELLIGENCE:
    - Wedding (masculine): Think sherwani, kurta pajama, bandhgala suit, indo-western — NOT plain formal shirts
    - Wedding (feminine): Think lehenga, saree, anarkali, ethnic coord, indo-western gown — NOT western casual
    - Office: Formal and structured — dress shirts, trousers, blazers
    - Party: Stylish and bold — statement pieces, trendy cuts
    - Date: Smart casual — clean, put-together but not overdressed
    - College: Casual and comfortable — jeans, tees, sneakers
    - Casual: Relaxed — anything comfortable

    Return ONLY valid JSON:
    {{
      "shirt": {{"color": "", "style": "", "fit": ""}} or null,
      "pants": {{"color": "", "style": "", "fit": ""}} or null,
      "overall_vibe": "",
      "vibe_emoji": "",
      "occasion_match_score": 0,
      "stylist_verdict": "",
      "occasion": "{occasion}",
      "gender": "{gender}"
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

    response = model.generate_content(contents)

    raw = response.text

    try:
        parsed = extract_json(raw)
        parsed.setdefault("vibe_emoji", "✨")
        parsed.setdefault("occasion_match_score", 0)
        parsed.setdefault("stylist_verdict", "This outfit needs a clearer stylist verdict.")
        parsed.setdefault("overall_vibe", "Unknown vibe")
        parsed.setdefault("occasion", occasion)
        parsed.setdefault("gender", gender)
        return parsed
    except Exception as e:
        print("JSON ERROR:", e)
        return {
            "shirt": None,
            "pants": None,
            "overall_vibe": "Unknown vibe",
            "vibe_emoji": "✨",
            "occasion_match_score": 0,
            "stylist_verdict": f"I could not confidently read this look for {occasion}, so treat the recommendations as a safer reset.",
            "occasion": occasion,
            "gender": gender
        }
