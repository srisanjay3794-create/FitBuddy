from app.config import get_settings
from app.gemini_client import generate_text

settings = get_settings()


def generate_nutrition_tip_with_flash(goal):
    prompt = f'''
You are FitBuddy, an AI fitness nutrition assistant.

Fitness goal: {goal}

Give one useful nutrition or recovery tip tailored to this goal.
Requirements:
- 3 to 5 sentences.
- Practical and easy to understand.
- No extreme diets.
- Do not diagnose medical conditions.
- Mention that individual nutritional needs can vary.
Return only the tip.
'''
    return generate_text(prompt, settings.gemini_nutrition_model)
