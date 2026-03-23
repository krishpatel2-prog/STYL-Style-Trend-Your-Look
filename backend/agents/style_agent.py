from google import genai
import os
from dotenv import load_dotenv
import json

from agents.vision_agent import extract_json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def recommend_outfit(vision_data: dict):
    has_shirt = vision_data.get("shirt") is not None
    has_pants = vision_data.get("pants") is not None

    if has_shirt and has_pants:
        task = "Recommend ONLY shoes to complete this outfit."
    elif has_shirt:
        task = "Recommend pants AND shoes to complete this outfit."
    elif has_pants:
        task = "Recommend shirt AND shoes to complete this outfit."
    else:
        return {"recommendations": {}}

    prompt = f"""
You are a fashion stylist AI.

User outfit:
Shirt: {json.dumps(vision_data.get('shirt'))}
Pants: {json.dumps(vision_data.get('pants'))}
Overall vibe: {vision_data.get('overall_vibe')}
Occasion: {vision_data.get('occasion')}

Task: {task}

STRICT:
- Always return at least 3 suggestions per category
- Do NOT return empty arrays
- For each item include: item name, reason it works, search_query for shopping

Return ONLY valid JSON:

{{
  "recommendations": {{
    "shirts": [
      {{"item": "", "reason": "", "search_query": ""}}
    ],
    "pants": [
      {{"item": "", "reason": "", "search_query": ""}}
    ],
    "shoes": [
      {{"item": "", "reason": "", "search_query": ""}}
    ]
  }}
}}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt]
    )

    raw = response.text

    try:
        return extract_json(raw)
    except:
        return {"recommendations": {}}