import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

from agents.vision_agent import extract_json

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def recommend_outfit(vision_data: dict, gender: str = "neutral"):
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
You are an expert fashion stylist with deep knowledge of color theory and occasion-appropriate dressing.

User outfit:
Shirt: {json.dumps(vision_data.get('shirt'))}
Pants: {json.dumps(vision_data.get('pants'))}
Overall vibe: {vision_data.get('overall_vibe')}
Occasion: {vision_data.get('occasion')}
Gender perspective: {gender}

Task: {task}

STRICT FASHION RULES YOU MUST FOLLOW:

COLOR HARMONY RULES:
- Black goes with: white, grey, beige, camel, burgundy, navy (NOT black on black unless streetwear)
- Navy goes with: white, light grey, beige, light pink (NOT black, NOT brown)
- White goes with: everything — navy, black, beige, pastels
- Beige/Camel goes with: white, brown, olive, burgundy (NOT navy or black)
- Grey goes with: white, black, navy, burgundy
- Brown goes with: beige, white, olive, mustard (NOT black, NOT navy)
- When in doubt — neutral shoes (white, beige, tan, black) are always safe

OCCASION-APPROPRIATE FOOTWEAR RULES:
- Date (casual): white sneakers, loafers, chelsea boots, mules
- Date (formal): heels, pointed flats, leather oxfords
- College: sneakers, canvas shoes, chunky soles
- Party: heels, block heels, dressy sandals, boots (female) / clean sneakers, loafers (male)
- Office: formal shoes, loafers, block heels, pointed flats — NO sneakers
- Wedding (female): heels, wedges, ethnic juttis, embellished sandals — NEVER sneakers or sports shoes
- Wedding (male): formal leather shoes, juttis, loafers — NEVER sneakers
- Casual: sneakers, sandals, slides, anything comfortable

GENDER-SPECIFIC RULES:
- Female + wedding/party: always suggest heels or dressy footwear
- Male + office/formal: always suggest leather shoes, never sneakers
- Female + casual/college: sneakers, flats, mules are fine

OCCASION + GENDER CLOTHING RULES:

Wedding (masculine/male):
- TOP: Sherwani, Kurta with jacket, Bandhgala suit, Indo-western kurta — NEVER plain western shirts
- BOTTOM: Churidar, Pajama, Dhoti pants, Well-fitted trousers for indo-western
- SHOES: Juttis, Mojaris, Formal leather shoes, Kolhapuris — NEVER sneakers
- search_query must include "wedding" and "ethnic" or "indo-western"

Wedding (feminine/female):
- OUTFIT: Lehenga, Saree, Anarkali suit, Sharara, Ethnic coord, Indo-western gown
- SHOES: Heels, Wedges, Embellished sandals, Ethnic juttis — NEVER sneakers or sports shoes
- search_query must include "wedding" and "ethnic" or "bridal"

Office (any gender):
- Clean, structured, professional pieces only
- NEVER suggest graphic tees, ripped jeans, hoodies, sneakers

Party (feminine):
- Bold, statement pieces — sequins, satin, bold colors
- Heels, block heels, strappy sandals

Party (masculine):
- Trendy but clean — printed shirts, chinos, dark jeans
- Chelsea boots, loafers, clean white sneakers

Date:
- Smart casual — elevated basics, clean cuts
- Not overdressed, not underdressed

College:
- Comfortable, trendy, youthful
- Jeans, casual tops, sneakers all fine

Beach/Casual:
- Relaxed, breathable fabrics
- Shorts, linen shirts, sandals, slides

Always suggest items that COMPLEMENT the existing colors — never clash.
Explain WHY each item works with the specific colors and occasion.

STRICT:
- Always return at least 3 suggestions per category
- Each suggestion must reference the actual colors in the outfit
- search_query must be specific and India-focused

Return ONLY valid JSON:
{{
  "recommendations": {{
    "shirts": [{{"item": "", "reason": "", "search_query": ""}}],
    "pants": [{{"item": "", "reason": "", "search_query": ""}}],
    "shoes": [{{"item": "", "reason": "", "search_query": ""}}]
  }}
}}
"""

    model = genai.GenerativeModel("gemini-2.5-flash")

    response = model.generate_content(prompt)

    raw = response.text

    try:
        return extract_json(raw)
    except:
        return {"recommendations": {}}
