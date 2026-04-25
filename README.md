Smart Food Recommender - Emotion + Logic Engine

Overview
This backend module converts user questionnaire answers into:
1) Mood (happy, stressed, tired, anxious, neutral)
2) Energy score (0 to 100)
3) Food intent (recommended food style)

Current focus
This project now uses one clean pipeline flow only.

Pipeline flow
1) `calculate_scores` from questionnaire answers
2) `get_energy_score` normalize to 0-100
3) `detect_mood` with simple rules
4) `classify_energy` to low/medium/high
5) `get_food_intent` from mood + energy level
6) `build_output` API-ready dictionary

Run options
- Quick run: `python src/main.py`
- Demo cases: `python src/demo_test_cases.py`
- Tests: `python -m pytest -q`

Folder structure
- src/emotion_engine: Core logic modules
- src/main.py: Pipeline runner example
- src/demo_test_cases.py: 3 project demonstration cases
- tests: Unit tests for logic functions
