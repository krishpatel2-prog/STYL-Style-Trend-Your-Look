import re
from typing import Any

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from agents.occasion_agent import plan_occasion_outfit
from agents.search_agent import enrich_recommendations, search_products
from agents.style_agent import recommend_outfit
from agents.vision_agent import analyze_outfit
from utils.image_utils import convert_to_base64


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/analyze")
async def analyze_fit(
    shirt: UploadFile = File(None),
    pants: UploadFile = File(None),
    occasion: str = Form(...),
    gender: str = Form("neutral")
):
    shirt_base64 = await convert_to_base64(shirt) if shirt else None
    pants_base64 = await convert_to_base64(pants) if pants else None

    vision_result = {
        "shirt": None,
        "pants": None,
        "overall_vibe": "unknown",
        "occasion": occasion,
        "gender": gender,
    }
    enriched = {"recommendations": {}}
    warnings: list[str] = []

    try:
        vision_result = analyze_outfit(shirt_base64, pants_base64, occasion, gender)
    except Exception as exc:
        print("analyze_outfit failed:", exc)
        warnings.append(f"Vision analysis unavailable: {exc}")

    try:
        recommendations = recommend_outfit(vision_result, gender)
        enriched = enrich_recommendations(recommendations)
    except Exception as exc:
        print("recommendation pipeline failed:", exc)
        warnings.append(f"Recommendations unavailable: {exc}")

    return {
        "vision": vision_result,
        "recommendations": enriched,
        "warnings": warnings,
    }


@app.post("/occasion")
async def occasion_stylist(
    occasion: str = Form(...),
    style: str = Form(...),
    gender: str = Form(...),
    budget_min: int = Form(...),
    budget_max: int = Form(...)
):
    plan = {"outfit_plan": {"items": []}}
    warnings: list[str] = []

    try:
        plan = plan_occasion_outfit(occasion, style, gender, budget_min, budget_max)
    except Exception as exc:
        print("plan_occasion_outfit failed:", exc)
        warnings.append(f"Outfit planning unavailable: {exc}")

    items = plan.get("outfit_plan", {}).get("items", [])
    enriched_items = []

    for item in items:
        estimated = item.get("estimated_price", 999999)
        products = safe_search_products(
            search_query=item.get("search_query", ""),
            max_price=estimated,
        )
        filtered = [
            product for product in products
            if product.get("price") and extract_price(product.get("price")) <= estimated * 1.2
        ]

        enriched_items.append({
            "item_type": item.get("item_type"),
            "description": item.get("description"),
            "reason": item.get("reason"),
            "estimated_price": estimated,
            "products": filtered if filtered else products[:2],
        })

    if not enriched_items:
        enriched_items = build_fallback_outfit(occasion, style, gender, budget_max)

    return {
        "occasion": occasion,
        "style": style,
        "gender": gender,
        "budget": f"INR {budget_min:,} - INR {budget_max:,}",
        "outfit": enriched_items,
        "warnings": warnings,
    }


def safe_search_products(search_query: str, max_price: int | None = None) -> list[dict[str, Any]]:
    if not search_query:
        return []

    try:
        return search_products(
            search_query=search_query,
            num_results=5,
            max_price=max_price,
        )
    except Exception as exc:
        print("search_products failed:", exc)
        return []


def build_fallback_outfit(occasion: str, style: str, gender: str, budget_max: int) -> list[dict[str, Any]]:
    per_item_budget = max(budget_max // 3, 1)
    defaults = [
        ("shirt", f"{style} shirt for {occasion}", "A reliable top layer to set the outfit direction."),
        ("pants", f"Tailored pants for {occasion}", "A clean base to keep the look balanced."),
        ("shoes", f"Versatile shoes for {occasion}", "Footwear that keeps the outfit grounded and wearable."),
    ]

    return [
        {
            "item_type": item_type,
            "description": description,
            "reason": f"{reason} Suggested for a {gender} {style.lower()} look.",
            "estimated_price": per_item_budget,
            "products": [],
        }
        for item_type, description, reason in defaults
    ]


def extract_price(price_str: str) -> int:
    cleaned = re.sub(r"[^\d]", "", price_str)
    return int(cleaned) if cleaned else 999999
