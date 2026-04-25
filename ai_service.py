from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def generate_ai_response(mood, energy, foods):
    # Convert food list to readable format
    food_names = [f["name"] for f in foods]
    food_list = "\n".join([f"- {name}" for name in food_names])

    # 🎯 TASK 4: Strong prompt design
    prompt = f"""
You are a helpful and friendly nutrition assistant.

User mood: {mood}
Energy level: {energy}

Recommended foods:
{food_list}

Instructions:
- Explain why these foods are suitable
- Keep tone based on mood:
    stressed → comforting
    happy → exciting
    tired → calm and gentle
    anxious → reassuring
- Keep response short (4–6 lines)
- Use simple human language
- Do NOT use complex medical terms

Give a clean and friendly explanation.
"""

    try:
        # 🎯 TASK 7: Safe API handling
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        output = response.text.strip()

        # 🎯 TASK 6: Clean formatting
        return f"💡 AI Suggestion:\n\n{output}"

    except Exception as e:
        return f"⚠️ Error: {str(e)}"