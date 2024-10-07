from fastapi import APIRouter

api_router = APIRouter()
from api.endpoints import job, task, user

api_router.include_router(user.router, prefix="/user", tags=["Пользователь"])
api_router.include_router(task.router, prefix="/task", tags=["Задача"])
api_router.include_router(job.router, prefix="/job", tags=["Работа"])