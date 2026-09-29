import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(str(BASE_DIR / '.env'))


class Settings:
    app_name = os.getenv('APP_NAME', 'FitBuddy - AI Fitness Plan Generator')
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    gemini_workout_model = os.getenv('WORKOUT_MODEL', 'gemini-3.5-flash')
    gemini_nutrition_model = os.getenv('NUTRITION_MODEL', 'gemini-3.5-flash')
    database_url = os.getenv(
        'DATABASE_URL',
        'sqlite:///' + str(BASE_DIR / 'fitbuddy.db')
    )


def get_settings():
    return Settings()
