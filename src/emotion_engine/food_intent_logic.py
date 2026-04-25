def decide_food_intent(mood: str, energy_score: int, hunger_level: int, time_available: int) -> str:
    """Maps emotional state + context into recommendation intent."""
    if hunger_level >= 4 and time_available <= 2:
        return "quick-energy meal"
    if mood in {"stressed", "anxious"}:
        return "comforting and calming food"
    if mood == "tired" or energy_score < 40:
        return "light high-protein meal"
    if mood == "happy" and energy_score >= 60:
        return "balanced exploratory meal"
    return "simple balanced meal"


def get_food_intent(mood: str, energy_level: str) -> dict:
    """Maps final mood + energy category to food intent details.

    Returns:
    {
        "food_type": "...",
        "keywords": ["...", "..."]
    }
    """
    mood_value = str(mood).strip().lower()
    energy_value = str(energy_level).strip().lower()

    # High stress-like moods with low energy prefer comfort and easy meals.
    if mood_value in {"stressed", "anxious"} and energy_value == "low":
        return {
            "food_type": "comfort food",
            "keywords": ["warm", "soothing", "easy to digest"],
        }

    # Tired + low energy should be light and easy to handle.
    if mood_value == "tired" and energy_value == "low":
        return {
            "food_type": "light food",
            "keywords": ["light", "simple", "quick"],
        }

    # Happy + high energy can try new experiences.
    if mood_value == "happy" and energy_value == "high":
        return {
            "food_type": "explore new food",
            "keywords": ["new cuisine", "creative", "variety"],
        }

    if energy_value == "low":
        return {
            "food_type": "easy balanced meal",
            "keywords": ["quick", "balanced", "comforting"],
        }

    if energy_value == "medium":
        return {
            "food_type": "balanced meal",
            "keywords": ["home-style", "nutritious", "moderate"],
        }

    if energy_value == "high":
        return {
            "food_type": "protein rich meal",
            "keywords": ["high protein", "fresh", "filling"],
        }

    return {
        "food_type": "simple meal",
        "keywords": ["simple", "balanced"],
    }
