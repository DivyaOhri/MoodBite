"""Demo test cases for Smart Food Recommender emotion engine.

Run:
    python src/demo_test_cases.py
"""

from emotion_engine.pipeline import process_user_input


def run_demo_cases() -> None:
    # Three sample scenarios for project demonstration.
    test_cases = [
        {
            "name": "Case 1 - Happy + High Energy",
            "input": {"q1": "A", "q2": "A", "q3": "A"},
            "expected": {
                "mood": "happy",
                "energy_level": "high",
                "food_type": "explore new food",
            },
        },
        {
            "name": "Case 2 - Stressed + Low Energy",
            "input": {"q1": "B", "q2": "C", "q3": "D"},
            "expected": {
                "mood": "stressed",
                "energy_level": "low",
                "food_type": "comfort food",
            },
        },
        {
            "name": "Case 3 - Tired + Low Energy",
            "input": {"q1": "C", "q2": "C", "q3": "B"},
            "expected": {
                "mood": "tired",
                "energy_level": "low",
                "food_type": "light food",
            },
        },
    ]

    print("=" * 72)
    print("SMART FOOD RECOMMENDER - DEMO TEST CASES")
    print("=" * 72)

    passed = 0

    for index, case in enumerate(test_cases, start=1):
        result = process_user_input(case["input"])

        checks = {
            "mood": result["mood"] == case["expected"]["mood"],
            "energy_level": result["energy_level"] == case["expected"]["energy_level"],
            "food_type": result["food_intent"]["food_type"] == case["expected"]["food_type"],
        }
        case_passed = all(checks.values())
        if case_passed:
            passed += 1

        print(f"\n{index}. {case['name']}")
        print("-" * 72)
        print(f"Input:    {case['input']}")
        print(f"Expected: {case['expected']}")
        print(
            "Actual:   "
            f"{{'mood': '{result['mood']}', "
            f"'energy_score': {result['energy_score']}, "
            f"'energy_level': '{result['energy_level']}', "
            f"'food_type': '{result['food_intent']['food_type']}'}}"
        )
        print(f"Status:   {'PASS' if case_passed else 'FAIL'}")

    print("\n" + "=" * 72)
    print(f"Summary: {passed}/{len(test_cases)} test cases passed")
    print("=" * 72)


if __name__ == "__main__":
    run_demo_cases()
