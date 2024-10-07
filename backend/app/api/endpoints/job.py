from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints import access_security
from api.schemas import JobCreateSchema
from database.db_helper import db_helper
from database.requests.job import crud

router = APIRouter()


@router.post("/jobs", summary="Создание новой работы", description="Эндпоинт для создания новой работы по задаче.")
async def create_job(
    job_data: JobCreateSchema,
    session: AsyncSession = Depends(db_helper.session_dependency),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    job = await crud.create_job_for_task(session, user_id=user_id, task_id=job_data.task_id, job_data=job_data.dict())
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена или доступ запрещен")
    return {"message": "Работа успешно создана", "job": job}


@router.put("/jobs/{job_id}", summary="Выполнение работы", description="Эндпоинт для выполнения работы по задаче.")
async def complete_job(
    job_id: int,
    session: AsyncSession = Depends(db_helper.session_dependency),
    credentials: JwtAuthorizationCredentials = Security(access_security)
):
    user_id = credentials["user_id"]
    job = await crud.mark_job_as_completed(session, user_id=user_id, job_id=job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работа не найдена или доступ запрещен")
    return {"message": "Работа выполнена", "job": job}