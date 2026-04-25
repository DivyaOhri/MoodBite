import os
import sys

import pytest

# Ensure src/ is importable when running tests from project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emotion_engine.scoring import (
    calculate_scores,
    classify_energy,
    detect_mood,
    get_energy_score,
)


def test_calculate_scores_valid_answers() -> None:
    answers = {"q1": "A", "q2": "C", "q3": "B"}
    result = calculate_scores(answers)

    assert result == {
        "mood_score": 3,
        "energy_score": 1,
        "stress_score": 1,
    }


def test_calculate_scores_accepts_lowercase_options() -> None:
    answers = {"q1": "b", "q2": "a", "q3": "d"}
    result = calculate_scores(answers)

    assert result == {
        "mood_score": 1,
        "energy_score": 3,
        "stress_score": 3,
    }


def test_calculate_scores_invalid_or_missing_defaults_to_zero() -> None:
    answers = {"q1": "Z"}
    result = calculate_scores(answers)

    assert result == {
        "mood_score": 0,
        "energy_score": 0,
        "stress_score": 0,
    }


def test_get_energy_score_high_state_is_high_value() -> None:
    scores = {
        "mood_score": 3,
        "energy_score": 3,
        "stress_score": 0,
    }
    result = get_energy_score(scores)

    assert result == 100


def test_get_energy_score_low_state_is_low_value() -> None:
    scores = {
        "mood_score": 0,
        "energy_score": 0,
        "stress_score": 3,
    }
    result = get_energy_score(scores)

    assert result == 0


def test_get_energy_score_balanced_state_is_mid_range() -> None:
    scores = {
        "mood_score": 1,
        "energy_score": 2,
        "stress_score": 1,
    }
    result = get_energy_score(scores)

    assert result == 57


def test_get_energy_score_clamps_unexpected_input_values() -> None:
    scores = {
        "mood_score": 99,
        "energy_score": -2,
        "stress_score": 100,
    }
    result = get_energy_score(scores)

    assert 0 <= result <= 100


@pytest.mark.parametrize(
    "scores, expected_mood",
    [
        ({"mood_score": 3, "energy_score": 3, "stress_score": 0}, "happy"),
        ({"mood_score": 0, "energy_score": 2, "stress_score": 3}, "stressed"),
        ({"mood_score": 1, "energy_score": 2, "stress_score": 2}, "anxious"),
        ({"mood_score": 1, "energy_score": 1, "stress_score": 1}, "tired"),
        ({"mood_score": 2, "energy_score": 2, "stress_score": 1}, "neutral"),
    ],
)
def test_detect_mood_returns_expected_label(scores: dict, expected_mood: str) -> None:
    assert detect_mood(scores) == expected_mood


@pytest.mark.parametrize(
    "energy_score, expected_category",
    [
        (0, "low"),
        (40, "low"),
        (41, "medium"),
        (70, "medium"),
        (71, "high"),
        (100, "high"),
    ],
)
def test_classify_energy_ranges(energy_score: int, expected_category: str) -> None:
    assert classify_energy(energy_score) == expected_category
