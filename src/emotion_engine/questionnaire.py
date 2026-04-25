"""Questionnaire definition for the Emotion + Logic Engine."""

# Student-friendly, multiple-choice questionnaire.
# This is the source of questions that can be served by an API later.
QUESTIONNAIRE = [
    {
        "id": "q1",
        "question": "Which feeling best describes you right now?",
        "options": {
            "A": "Happy and positive",
            "B": "Stressed or under pressure",
            "C": "Sad or low",
            "D": "Anxious or worried",
        },
    },
    {
        "id": "q2",
        "question": "How is your energy level right now?",
        "options": {
            "A": "High - I feel active and focused",
            "B": "Medium - I can work, but not at my best",
            "C": "Low - I feel tired and slow",
        },
    },
    {
        "id": "q3",
        "question": "How stressed do you feel about studies or work today?",
        "options": {
            "A": "Low stress",
            "B": "Moderate stress",
            "C": "High stress",
            "D": "Very high stress",
        },
    },
    {
        "id": "q4",
        "question": "How mentally clear do you feel right now?",
        "options": {
            "A": "Very clear and focused",
            "B": "Mostly clear",
            "C": "A bit distracted",
            "D": "Very distracted or overwhelmed",
        },
    },
    {
        "id": "q5",
        "question": "How motivated are you to prepare food right now?",
        "options": {
            "A": "High - I can cook properly",
            "B": "Medium - I can make something simple",
            "C": "Low - I need something very quick",
        },
    },
]
