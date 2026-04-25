import os
import sys

# Ensure src/ is importable when running tests from project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emotion_engine.output_builder import build_output


def test_build_output_returns_expected_schema() -> None:
    result = build_output(
        mood="happy",
        energy_score=82,
        energy_level="high",
        food_intent={
            "food_type": "explore new food",
            "keywords": ["new cuisine", "creative"],
        },
    )

    assert result == {
        "mood": "happy",
        "energy_score": 82,
        "energy_level": "high",
        "food_intent": {
            "food_type": "explore new food",
            "keywords": ["new cuisine", "creative"],
        },
    }


def test_build_output_handles_missing_food_intent_fields() -> None:
    result = build_output(
        mood="neutral",
        energy_score=55,
        energy_level="medium",
        food_intent={},
    )

    assert result["food_intent"]["food_type"] == "simple meal"
    assert result["food_intent"]["keywords"] == ["simple", "balanced"]
