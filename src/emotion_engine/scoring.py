"""Questionnaire scoring helpers.

This module converts simple multiple-choice answers (A/B/C/D)
into numerical scores that the backend can use for logic.
"""

from typing import Dict


# Q1 mood option mapping.
# We keep mood labels and also convert to a numeric score.
MOOD_LABEL_MAP = {
    "A": "happy",
    "B": "stressed",
    "C": "sad",
    "D": "anxious",
}


# Numeric mapping for mood intensity score.
# Higher means more positive mood in this simple scale.
MOOD_SCORE_MAP = {
    "A": 3,
    "B": 1,
    "C": 0,
    "D": 0,
}


# Q2 energy mapping (A=high, B=medium, C=low).
ENERGY_SCORE_MAP = {
    "A": 3,
    "B": 2,
    "C": 1,
}


# Q3 stress mapping (A=low, B=moderate, C=high, D=very high).
# Higher value means higher stress.
STRESS_SCORE_MAP = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}


def _normalize_option(value: str) -> str:
    """Normalizes option text to uppercase letter form."""
    return str(value).strip().upper()


def calculate_scores(answers: dict) -> Dict[str, int]:
    """Converts questionnaire answers into numeric scores.

    Expected input shape:
    {
        "q1": "A",  # mood
        "q2": "C",  # energy
        "q3": "B",  # stress
    }

    Rules used:
    - Q1 maps mood choice to mood_score using MOOD_SCORE_MAP.
    - Q2 maps directly to energy_score using ENERGY_SCORE_MAP.
    - Q3 maps directly to stress_score using STRESS_SCORE_MAP.

    If an answer is missing or invalid, this function uses a safe default of 0.
    """
    q1 = _normalize_option(answers.get("q1", ""))
    q2 = _normalize_option(answers.get("q2", ""))
    q3 = _normalize_option(answers.get("q3", ""))

    return {
        "mood_score": MOOD_SCORE_MAP.get(q1, 0),
        "energy_score": ENERGY_SCORE_MAP.get(q2, 0),
        "stress_score": STRESS_SCORE_MAP.get(q3, 0),
    }


def get_energy_score(scores: dict) -> int:
    """Builds a final normalized energy score (0-100).

    Inputs expected in `scores`:
    - mood_score: 0 to 3 (higher is better)
    - energy_score: 0 to 3 (higher is better)
    - stress_score: 0 to 3 (higher means more stress, so it reduces energy)

    Calculation idea (simple and explainable):
    - Give more weight to direct energy answer.
    - Give medium weight to mood.
    - Convert stress into a positive "calmness" factor using (3 - stress).
    - Normalize weighted total to 0-100.
    """
    mood = int(scores.get("mood_score", 0))
    energy = int(scores.get("energy_score", 0))
    stress = int(scores.get("stress_score", 0))

    # Clamp each input to expected range to keep output stable.
    mood = max(0, min(3, mood))
    energy = max(0, min(3, energy))
    stress = max(0, min(3, stress))

    # Convert stress into a positive factor where higher is better.
    calmness = 3 - stress

    # Weighted raw score:
    # - energy has strongest impact
    # - mood and calmness support it
    raw_score = (energy * 3) + (mood * 2) + (calmness * 2)

    # Max possible raw score is 21: (3*3) + (3*2) + (3*2)
    max_raw_score = 21
    normalized = round((raw_score / max_raw_score) * 100)

    return max(0, min(100, normalized))


def detect_mood(scores: dict) -> str:
    """Determines final mood label using simple if-else rules.

    Inputs expected in `scores`:
    - mood_score: 0 to 3 (higher means better mood)
    - stress_score: 0 to 3 (higher means more stress)
    - energy_score: 0 to 3 (used only for tired rule)

    Rule summary:
    - very high stress -> stressed
    - moderate stress with low mood -> anxious
    - low energy + low mood -> tired
    - high mood with low stress -> happy
    - otherwise -> neutral
    """
    mood = int(scores.get("mood_score", 0))
    stress = int(scores.get("stress_score", 0))
    energy = int(scores.get("energy_score", 0))

    # Clamp inputs so unexpected values do not break the rules.
    mood = max(0, min(3, mood))
    stress = max(0, min(3, stress))
    energy = max(0, min(3, energy))

    if stress >= 3:
        return "stressed"
    if stress == 2 and mood <= 1:
        return "anxious"
    if energy <= 1 and mood <= 1:
        return "tired"
    if mood >= 3 and stress <= 1:
        return "happy"
    return "neutral"


def classify_energy(energy_score: int) -> str:
    """Classifies normalized energy score into low/medium/high.

    Categories:
    - low: 0 to 40
    - medium: 41 to 70
    - high: 71 to 100
    """
    score = int(energy_score)
    score = max(0, min(100, score))

    if score <= 40:
        return "low"
    if score <= 70:
        return "medium"
    return "high"
