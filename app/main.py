from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import BASE_DIR, get_settings
from app.database import init_db
from app.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    description='AI-powered 7-day fitness plan generator',
    lifespan=lifespan,
)

app.mount(
    '/static',
    StaticFiles(directory=str(BASE_DIR / 'static')),
    name='static',
)

app.include_router(router)
