from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.config import BASE_DIR
from app.database import (
    get_db,
    get_latest_plan,
    get_user,
    get_all_users,
    save_plan,
    save_user,
    update_plan,
    delete_user,
)
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))


@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


@router.post('/generate-workout', response_class=HTMLResponse)
def generate_workout(
    request: Request,
    name: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        existing = get_user(db, user_id)
        data = {
            'user_id': user_id.strip(),
            'name': name.strip(),
            'age': age,
            'weight': weight,
            'goal': goal.strip(),
            'intensity': intensity.strip(),
        }

        if existing:
            existing.name = data['name']
            existing.age = data['age']
            existing.weight = data['weight']
            existing.goal = data['goal']
            existing.intensity = data['intensity']
            db.commit()
            db.refresh(existing)
            user = existing
        else:
            user = save_user(db, data)

        workout_plan = generate_workout_gemini(
            name=data['name'],
            user_id=data['user_id'],
            age=data['age'],
            weight=data['weight'],
            goal=data['goal'],
            intensity=data['intensity'],
        )
        nutrition_tip = generate_nutrition_tip_with_flash(data['goal'])
        plan = save_plan(db, user.id, workout_plan, nutrition_tip)

        return templates.TemplateResponse(
            'result.html',
            {
                'request': request,
                'user': user,
                'plan': plan,
                'workout_plan': workout_plan,
                'nutrition_tip': nutrition_tip,
                'error': None,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            'error.html',
            {'request': request, 'error': str(exc)},
            status_code=500,
        )


@router.post('/submit-feedback', response_class=HTMLResponse)
def submit_feedback(
    request: Request,
    user_id: str = Form(...),
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        user = get_user(db, user_id)
        plan = get_latest_plan(db, user_id)
        if not user or not plan:
            raise ValueError('User or workout plan was not found.')

        revised = update_workout_plan(
            original_plan=plan.original_plan,
            feedback=feedback,
            name=user.name,
            goal=user.goal,
            intensity=user.intensity,
        )
        update_plan(db, plan, revised, feedback)

        return templates.TemplateResponse(
            'result.html',
            {
                'request': request,
                'user': user,
                'plan': plan,
                'workout_plan': revised,
                'nutrition_tip': plan.nutrition_tip,
                'error': None,
            },
        )
    except Exception as exc:
        return templates.TemplateResponse(
            'error.html',
            {'request': request, 'error': str(exc)},
            status_code=500,
        )


@router.get('/view-all-users', response_class=HTMLResponse)
def view_all_users(request: Request, db: Session = Depends(get_db)):
    users = get_all_users(db)
    return templates.TemplateResponse(
        'all_users.html',
        {'request': request, 'users': users},
    )


@router.post('/delete-user/{user_id}')
def remove_user(user_id: str, db: Session = Depends(get_db)):
    delete_user(db, user_id)
    return RedirectResponse('/view-all-users', status_code=303)
