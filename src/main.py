from emotion_engine.pipeline import process_user_input


if __name__ == "__main__":
    # Example answers from questionnaire options.
    sample_answers = {
        "q1": "B",
        "q2": "C",
        "q3": "D",
    }

    result = process_user_input(sample_answers)
    print("Final Output:")
    print(result)
