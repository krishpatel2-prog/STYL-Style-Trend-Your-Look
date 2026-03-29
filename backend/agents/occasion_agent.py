import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from .vision_agent import extract_json


load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def plan_occasion_outfit(occasion: str, style: str, gender: str, budget_min: int, budget_max: int):
    prompt = f"""
    You are an expert fashion stylist with deep knowledge of color theory, occasion-appropriate dressing, and Indian fashion market.

    User Request:
    - Occasion: {occasion}
    - Style preference: {style}
    - Gender: {gender}
    - Budget range: ₹{budget_min} - ₹{budget_max} total

    Plan a COMPLETE, COHESIVE outfit where every piece works together harmoniously.

    STRICT BUDGET RULES:
    - Total outfit cost MUST be under ₹{budget_max}
    - Shirt budget: ₹{int(budget_max * 0.35)}
    - Pants budget: ₹{int(budget_max * 0.35)}
    - Shoes budget: ₹{int(budget_max * 0.25)}
    - Accessory budget: ₹{int(budget_max * 0.05)}
    - Each item MUST be under its allocated budget

    COLOR HARMONY RULES YOU MUST FOLLOW:
    - Black top: pair with white, grey, beige, camel, olive, burgundy bottoms — NEVER navy
    - Navy top: pair with white, light grey, beige, khaki bottoms — NEVER black or brown
    - White top: pairs with everything — navy, black, beige, pastels, earth tones
    - Beige/Camel top: pair with white, brown, olive, burgundy, rust bottoms — NEVER navy or black
    - Grey top: pair with white, black, navy, burgundy, mustard bottoms
    - Brown/Rust top: pair with beige, white, olive, cream bottoms — NEVER navy or black
    - Pastel top: pair with white, nude, light grey, or matching pastel bottoms
    - Bold/printed top: pair with neutral solid bottoms — black, white, beige, navy
    - When colors could clash — always default to neutral bottoms (beige, white, black, grey)
    - Shoes should complement BOTH top and bottom — pick a color that ties the look together

    OCCASION-APPROPRIATE RULES:
    Date (casual): relaxed but put-together — jeans/chinos, clean top, loafers/white sneakers/mules
    Date (formal): elevated smart casual — trousers, formal shirt/blouse, heels/leather shoes
    College: comfortable and trendy — jeans, casual tops, sneakers/canvas shoes
    Party: stylish and bold — statement pieces, heels/boots (female), clean sneakers/loafers (male)
    Office: professional — formal trousers/skirts, formal shirts/blouses, leather shoes/block heels — ABSOLUTELY NO sneakers
    Wedding (female): elegant and dressy — saree/lehenga/anarkali/ethnic coord OR formal gown/dress, heels/wedges/juttis/embellished sandals — NEVER sneakers or sports shoes EVER
    Wedding (male): formal ethnic or western — sherwani/kurta pajama/suit, juttis/formal leather shoes/loafers — NEVER sneakers
    Casual: anything comfortable and relaxed — jeans, tees, sneakers/sandals/slides

    GENDER-SPECIFIC RULES:
    Female:
    - Wedding/Party: ALWAYS suggest heels, wedges, block heels, embellished flats or ethnic footwear
    - Office: pointed flats, block heels, loafers — no sneakers
    - Casual/College: sneakers, flats, mules, sandals all fine
    - Suggest feminine cuts: crop tops, blouses, fitted shirts, flowy tops

    Male:
    - Wedding/Formal: leather shoes, juttis, loafers — NEVER sneakers
    - Office: formal leather shoes, loafers — NEVER sneakers
    - Casual/College/Party: sneakers, loafers, casual shoes fine
    - Suggest masculine cuts: regular/slim fit shirts, polos, tees

    STYLE AESTHETIC RULES:
    - Classic: timeless pieces, neutral colors, clean cuts, no bold prints
    - Minimalist: neutral palette (white/black/grey/beige), simple silhouettes, no logos
    - Streetwear: oversized fits, bold colors, graphic elements, chunky sneakers
    - GenZ: trendy cuts, color mixing, crop tops, wide legs, platform shoes
    - Smart Casual: elevated basics, chinos/trousers, collared shirts, clean shoes
    - Formal: structured pieces, dark or neutral tones, dress shoes

    COHESION RULE:
    Before finalizing — mentally check: do all 3 items (shirt + pants + shoes) work together as a complete look? Do the colors complement each other? Is the formality level consistent across all pieces?

    STRICT OUTPUT RULES:
    - Always include: shirt, pants, shoes
    - Optionally include one accessory if budget allows
    - Each item MUST reference why it works with the OTHER items in the outfit
    - search_query must be specific, India-focused, and include gender

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
    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    raw = response.text

    try:
        return extract_json(raw)
    except:
        return {"outfit_plan": {}}
