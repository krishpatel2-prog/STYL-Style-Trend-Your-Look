from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")


def search_products(search_query: str, num_results: int = 3, max_price: int = None):
    query = search_query
    if max_price:
        query = f"{search_query} under ₹{max_price}"

    params = {
        "engine": "google_shopping",
        "q": query,
        "api_key": SERPAPI_KEY,
        "gl": "in",
        "hl": "en",
        "num": num_results
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    shopping_results = results.get("shopping_results", [])

    products = []
    for item in shopping_results[:num_results]:
        products.append({
            "title": item.get("title"),
            "price": item.get("price"),
            "source": item.get("source"),
            "link": item.get("product_link") or item.get("link") or item.get("serpapi_product_api"),
            "thumbnail": item.get("thumbnail")
        })

    return products


def enrich_recommendations(recommendations: dict):
    enriched = {}

    for category, items in recommendations.get("recommendations", {}).items():
        enriched[category] = []
        for item in items:
            products = search_products(item.get("search_query", ""))
            enriched[category].append({
                "item": item.get("item"),
                "reason": item.get("reason"),
                "products": products
            })

    return {"recommendations": enriched}
