"""Helpers to build consistent API-ready output payloads."""


def build_output(mood, energy_score, energy_level, food_intent) -> dict:
    """Builds final response schema used by backend APIs.

    Expected output:
    {
      "mood": "...",
      "energy_score": number,
      "energy_level": "...",
      "food_intent": {
          "food_type": "...",
          "keywords": [...]
      }
    }
    """
    # Keep output stable even if upstream passes unexpected types.
    safe_food_intent = food_intent if isinstance(food_intent, dict) else {}
    food_type = str(safe_food_intent.get("food_type", "simple meal"))
    keywords = safe_food_intent.get("keywords", ["simple", "balanced"])

    if not isinstance(keywords, list):
        keywords = [str(keywords)]

    return {
        "mood": str(mood),
        "energy_score": int(energy_score),
        "energy_level": str(energy_level),
        "food_intent": {
            "food_type": food_type,
            "keywords": [str(item) for item in keywords],
        },
    }
