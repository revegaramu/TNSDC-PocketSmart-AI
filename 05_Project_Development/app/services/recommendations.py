import json
import re
from typing import Any

from google import genai

from app.config import settings


def _extract_json(text: str) -> dict[str, Any]:
    """Parse JSON returned by the model, including fenced JSON."""
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    start = cleaned.find("{")
    end = cleaned.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("The AI response did not contain JSON.")

    return json.loads(cleaned[start : end + 1])


def _fallback(category: str, data: dict[str, Any]) -> dict[str, Any]:
    budget = float(data.get("budget", 0))
    notes = str(data.get("notes", "")).strip()

    if category == "home":
        title = f"{data['style']} {data['room_type']} plan"
        items = [
            {
                "name": "Essential furniture",
                "description": "Prioritize practical, durable furniture.",
                "estimated_cost": round(budget * 0.40, 2),
            },
            {
                "name": "Lighting",
                "description": "Use layered lighting for comfort.",
                "estimated_cost": round(budget * 0.15, 2),
            },
            {
                "name": "Storage",
                "description": "Choose storage that fits the room.",
                "estimated_cost": round(budget * 0.20, 2),
            },
            {
                "name": "Decor and finishing",
                "description": "Add textiles, artwork, and small accents.",
                "estimated_cost": round(budget * 0.15, 2),
            },
            {
                "name": "Contingency",
                "description": "Keep a reserve for unexpected expenses.",
                "estimated_cost": round(budget * 0.10, 2),
            },
        ]

    elif category == "party":
        title = f"{data['occasion']} event plan"
        items = [
            {
                "name": "Venue and setup",
                "description": "Choose a suitable venue and seating layout.",
                "estimated_cost": round(budget * 0.25, 2),
            },
            {
                "name": "Food and refreshments",
                "description": "Plan portions around the guest count.",
                "estimated_cost": round(budget * 0.35, 2),
            },
            {
                "name": "Decorations",
                "description": "Use a consistent theme and simple decor.",
                "estimated_cost": round(budget * 0.15, 2),
            },
            {
                "name": "Entertainment",
                "description": "Choose activities appropriate for guests.",
                "estimated_cost": round(budget * 0.15, 2),
            },
            {
                "name": "Contingency",
                "description": "Reserve funds for unexpected costs.",
                "estimated_cost": round(budget * 0.10, 2),
            },
        ]

    else:
        title = f"Jewelry suggestions for {data['occasion']}"
        items = [
            {
                "name": "Earrings",
                "description": (
                    f"Explore designs that complement "
                    f"{data['outfit_color']} clothing."
                ),
                "estimated_cost": round(budget * 0.25, 2),
            },
            {
                "name": "Necklace",
                "description": "Choose a style suited to the outfit neckline.",
                "estimated_cost": round(budget * 0.35, 2),
            },
            {
                "name": "Bracelet or bangles",
                "description": "Consider a coordinated accessory.",
                "estimated_cost": round(budget * 0.20, 2),
            },
            {
                "name": "Optional accessory",
                "description": "Choose a complementary ring or hair accessory.",
                "estimated_cost": round(budget * 0.10, 2),
            },
            {
                "name": "Budget reserve",
                "description": "Keep some budget for price variations.",
                "estimated_cost": round(budget * 0.10, 2),
            },
        ]

    return {
        "title": title,
        "summary": (
            "These are general planning suggestions, not live product "
            "quotes. Verify availability and prices before purchasing."
        ),
        "items": items,
        "estimated_total": round(
            sum(item["estimated_cost"] for item in items), 2
        ),
        "tips": [
            "Compare prices from multiple sellers.",
            "Keep the total within your stated budget.",
            "Confirm product quality, availability, and return policies.",
        ],
        "shopping_links": [],
        "notes": notes,
        "ai_provider": "local",
    }


def _build_prompt(category: str, data: dict[str, Any]) -> str:
    return f"""
You are PocketSmart AI, a practical budgeting assistant.

Create a useful recommendation for category: {category}.
User preferences:
{json.dumps(data, ensure_ascii=False)}

Return ONLY valid JSON with this structure:
{{
  "title": "Short title",
  "summary": "A concise explanation",
  "items": [
    {{
      "name": "Item name",
      "description": "Practical explanation",
      "estimated_cost": 100
    }}
  ],
  "estimated_total": 100,
  "tips": ["Tip 1", "Tip 2"],
  "shopping_links": []
}}

Rules:
- All costs must be non-negative numbers in the user's budget currency.
- Do not claim that prices or stock were checked live.
- Do not invent product URLs.
- Keep the estimated total within the user's budget.
- Give 3 to 8 useful items.
- Return JSON only.
"""


def generate_recommendation(
    category: str,
    data: dict[str, Any],
) -> dict[str, Any]:
    """Use Gemini when configured; otherwise use local recommendations."""
    if not settings.GEMINI_API_KEY:
        return _fallback(category, data)

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=_build_prompt(category, data),
            config={
                "response_mime_type": "application/json",
            },
        )

        result = _extract_json(response.text or "")

        if not isinstance(result.get("items"), list):
            raise ValueError("AI response has no items list.")

        budget = float(data["budget"])
        total = sum(
            max(0, float(item.get("estimated_cost", 0)))
            for item in result["items"]
        )

        if total > budget:
            result["summary"] = (
                str(result.get("summary", ""))
                + " Review individual estimates to remain within budget."
            )

        result["estimated_total"] = round(total, 2)
        result["ai_provider"] = "gemini"
        result.setdefault("tips", [])
        result.setdefault("shopping_links", [])

        return result

    except Exception:
        # Keep the app usable if the API key, model, network, or response
        # is unavailable. Do not expose provider errors to the user.
        return _fallback(category, data)


def generate_image_aware_jewelry_recommendation(
    data: dict[str, Any],
    image_bytes: bytes | None = None,
    mime_type: str = "image/jpeg",
) -> dict[str, Any]:
    """
    Use the same recommendation pipeline for jewelry.

    Image uploads are accepted by the API, but this function currently
    uses the user's written outfit description. This keeps the basic
    application functional without requiring a multimodal model call.
    """
    result = generate_recommendation("jewelry", data)

    if image_bytes:
        result["summary"] += (
            " An outfit image was uploaded, but this version does not "
            "perform visual image analysis."
        )

    return result