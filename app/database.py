from datetime import datetime
from typing import List, Optional

from sqlalchemy import create_engine, String, Integer, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

from app.config import get_settings

settings = get_settings()
connect_args = {'check_same_thread': False} if settings.database_url.startswith('sqlite') else {}
engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    age: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    goal: Mapped[str] = mapped_column(String(50))
    intensity: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    plans: Mapped[List['WorkoutPlan']] = relationship(
        back_populates='user', cascade='all, delete-orphan'
    )


class WorkoutPlan(Base):
    __tablename__ = 'workout_plans'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE'), index=True
    )
    original_plan: Mapped[str] = mapped_column(Text)
    updated_plan: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    nutrition_tip: Mapped[str] = mapped_column(Text)
    feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    user: Mapped[User] = relationship(back_populates='plans')


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_user(db, data):
    user = User(**data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db, user_id):
    return db.query(User).filter(User.user_id == user_id).first()


def save_plan(db, user_pk, original_plan, nutrition_tip):
    plan = WorkoutPlan(
        user_id=user_pk,
        original_plan=original_plan,
        nutrition_tip=nutrition_tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_latest_plan(db, user_id):
    return (
        db.query(WorkoutPlan)
        .join(User)
        .filter(User.user_id == user_id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )


def update_plan(db, plan, updated_plan, feedback):
    plan.updated_plan = updated_plan
    plan.feedback = feedback
    db.commit()
    db.refresh(plan)
    return plan


def get_all_users(db):
    return db.query(User).order_by(User.created_at.desc()).all()


def delete_user(db, user_id):
    user = get_user(db, user_id)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
