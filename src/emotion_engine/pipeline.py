"""End-to-end processing pipeline for questionnaire answers."""

from .food_intent_logic import get_food_intent
from .output_builder import build_output
from .scoring import calculate_scores, classify_energy, detect_mood, get_energy_score


def process_user_input(answers: dict) -> dict:
    """Runs the full emotion + logic flow and returns final output.

    Pipeline steps:
    1) Calculate base scores from options
    2) Compute normalized energy score (0-100)
    3) Detect final mood label
    4) Classify energy level (low/medium/high)
    5) Map mood + energy to food intent
    6) Build API-ready response schema
    """
    # Step 1: convert answer options (A/B/C/D) into numeric scores.
    scores = calculate_scores(answers)

    # Step 2: derive normalized final energy score.
    energy_score = get_energy_score(scores)

    # Step 3: detect mood using rule-based logic.
    mood = detect_mood(scores)

    # Step 4: convert numeric energy into category label.
    energy_level = classify_energy(energy_score)

    # Step 5: get recommended food intent from mood + energy category.
    food_intent = get_food_intent(mood, energy_level)

    # Step 6: return a clean output object for backend/API usage.
    return build_output(
        mood=mood,
        energy_score=energy_score,
        energy_level=energy_level,
        food_intent=food_intent,
    )
