from app.config import get_settings
from app.gemini_client import generate_text

settings = get_settings()


def update_workout_plan(original_plan, feedback, name, goal, intensity):
    prompt = f'''
You are FitBuddy.

Update an existing 7-day workout plan based on user feedback.

User name: {name}
Goal: {goal}
Intensity: {intensity}

ORIGINAL PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Create a complete revised 7-day workout plan.
Requirements:
- Keep useful parts of the original plan.
- Apply the feedback.
- Include DAY 1 through DAY 7.
- Include warm-up, exercises, sets/repetitions or duration, rest, and cooldown/recovery.
- Avoid dangerous or extreme recommendations.
- Do not diagnose medical conditions.
- Return only the revised workout plan.
'''
    return generate_text(prompt, settings.gemini_workout_model)
