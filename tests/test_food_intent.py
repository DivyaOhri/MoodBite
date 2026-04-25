import os
import sys

import pytest

# Ensure src/ is importable when running tests from project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emotion_engine.food_intent_logic import get_food_intent


@pytest.mark.parametrize(
    "mood, energy_level, expected_food_type",
    [
        ("stressed", "low", "comfort food"),
        ("tired", "low", "light food"),
        ("happy", "high", "explore new food"),
        ("neutral", "medium", "balanced meal"),
        ("anxious", "high", "protein rich meal"),
    ],
)
def test_get_food_intent_mapping(mood: str, energy_level: str, expected_food_type: str) -> None:
    result = get_food_intent(mood, energy_level)

    assert result["food_type"] == expected_food_type
    assert isinstance(result["keywords"], list)
    assert len(result["keywords"]) >= 2


def test_get_food_intent_unknown_energy_has_safe_default() -> None:
    result = get_food_intent("happy", "unknown")

    assert result["food_type"] == "simple meal"
    assert result["keywords"] == ["simple", "balanced"]
