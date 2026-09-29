from app.config import get_settings
from app.gemini_client import generate_text

settings = get_settings()


def generate_workout_gemini(
    name: str,
    user_id: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    prompt = f'''
You are FitBuddy, a careful AI fitness-planning assistant.

Create a personalized 7-day workout plan.

USER INFORMATION
Name: {name}
User ID: {user_id}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

REQUIREMENTS
1. Generate exactly 7 days.
2. Give each day a clear heading.
3. Include the workout focus.
4. Include warm-up.
5. Include main exercises.
6. Include sets and repetitions or duration.
7. Include rest guidance.
8. Include cooldown or recovery guidance.
9. Include at least one rest/recovery day.
10. Gradually progress through the week.
11. Adapt the plan to the user's goal and requested intensity.
12. Do not assume gym equipment; give bodyweight alternatives where useful.
13. Do not prescribe medications or diagnose medical conditions.
14. Avoid dangerous or extreme recommendations.
15. Keep the plan practical and easy to understand.

FORMAT
DAY 1
Focus:
Warm-up:
Main Workout:
Rest:
Cooldown:

Repeat the same structure through DAY 7.

End with a short safety note recommending professional advice for injuries, medical conditions, pregnancy, or uncertainty.
Return only the workout plan.
'''
    return generate_text(prompt, settings.gemini_workout_model)
