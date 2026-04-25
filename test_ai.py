from ai_service import generate_ai_response

foods = [
    {"name": "banana"},
    {"name": "milk"},
    {"name": "nuts"}
]

result = generate_ai_response("tired", "low", foods)
print(result)