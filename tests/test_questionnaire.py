import os
import sys

# Ensure src/ is importable when running tests from project root.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from emotion_engine.questionnaire import QUESTIONNAIRE


def test_questionnaire_has_required_questions() -> None:
    assert len(QUESTIONNAIRE) == 5
    assert [item["id"] for item in QUESTIONNAIRE] == ["q1", "q2", "q3", "q4", "q5"]


def test_questionnaire_options_are_multiple_choice() -> None:
    for item in QUESTIONNAIRE:
        assert "question" in item
        assert "options" in item
        assert isinstance(item["options"], dict)
        assert len(item["options"]) >= 3
