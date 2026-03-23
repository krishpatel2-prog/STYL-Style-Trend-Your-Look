from google import genai
import os
from dotenv import load_dotenv
import json
from agents.vision_agent import extract_json


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def plan_occasion_outfit(occasion: str, style: str, gender: str, budget_min: int, budget_max: int):
    prompt = f"""
    You are a fashion stylist AI.

    User Request:
    - Occasion: {occasion}
    - Style preference: {style}
    - Gender: {gender}
    - Budget range: ₹{budget_min} - ₹{budget_max} total

    Plan a COMPLETE outfit for this person.

    STRICT:
    - Total outfit cost MUST be under ₹{budget_max}
    - Split budget: 35% shirt, 35% pants, 25% shoes, 5% accessory
    - Shirt budget: ₹{int(budget_max * 0.35)}
    - Pants budget: ₹{int(budget_max * 0.35)}
    - Shoes budget: ₹{int(budget_max * 0.25)}
    - Accessory budget: ₹{int(budget_max * 0.05)}
    - Each item MUST be under its allocated budget above
    - Suggest items appropriate for {gender}
    - Match the {style} aesthetic
    - Always include: shirt, pants, shoes
    - Optionally include: accessory

    For each item include:
    - item_type
    - description
    - reason it fits occasion and style
    - estimated_price in INR (MUST be under allocated budget)
    - search_query optimized for Google Shopping India

    Return ONLY valid JSON:

    {{
      "outfit_plan": {{
        "occasion": "{occasion}",
        "style": "{style}",
        "total_budget": {budget_max},
        "items": [
          {{
            "item_type": "",
            "description": "",
            "reason": "",
            "estimated_price": 0,
            "search_query": ""
          }}
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
        return {"outfit_plan": {}}