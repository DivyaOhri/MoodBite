import os
import sys

# Ensure src/ is importable when running tests from project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emotion_engine.pipeline import process_user_input


def test_process_user_input_returns_expected_structure() -> None:
    result = process_user_input({"q1": "A", "q2": "B", "q3": "A"})

    assert set(result.keys()) == {"mood", "energy_score", "energy_level", "food_intent"}
    assert result["mood"] in {"happy", "stressed", "tired", "anxious", "neutral"}
    assert 0 <= result["energy_score"] <= 100
    assert result["energy_level"] in {"low", "medium", "high"}
    assert isinstance(result["food_intent"], dict)
    assert "food_type" in result["food_intent"]
    assert "keywords" in result["food_intent"]


def test_process_user_input_example_stressed_low_maps_to_comfort_food() -> None:
    # q1=B -> mood_score=1, q2=C -> energy_score=1, q3=D -> stress_score=3
    # This should produce low energy and stressed mood in the current rules.
    result = process_user_input({"q1": "B", "q2": "C", "q3": "D"})

    assert result["mood"] == "stressed"
    assert result["energy_level"] == "low"
    assert result["food_intent"]["food_type"] == "comfort food"
