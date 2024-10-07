from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi_jwt import JwtAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api.endpoints import access_security
from api.schemas import TaskCreateSchema
from database.requests.task import crud
from database.db_helper import db_helper

router = APIRouter()


@router.get("/tasks", summary="Получение списка задач", description="Эндпоинт для получения всех задач пользователя.")
async def get_tasks(user_id: int, session: AsyncSession = Depends(db_helper.session_dependency), credentials: JwtAuthorizationCredentials = Security(access_security)):
    tasks = await crud.get_user_tasks(session, user_id)
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задачи не найдены")
    return {"tasks": tasks}


@router.post("/tasks", summary="Создание новой задачи", description="Эндпоинт для создания новой задачи.")
async def create_task(task_data: TaskCreateSchema, session: AsyncSession = Depends(db_helper.session_dependency), credentials: JwtAuthorizationCredentials = Security(access_security)):
    new_task = await crud.create_user_task(session, task_data.user_id, task_data.dict())
    return {"message": "Задача успешно создана", "task": new_task}


@router.get("/tasks/{task_id}", summary="Получение задачи по ID", description="Эндпоинт для получения задачи по идентификатору.")
async def get_task(task_id: int, user_id: int, session: AsyncSession = Depends(db_helper.session_dependency), credentials: JwtAuthorizationCredentials = Security(access_security)):
    task = await crud.get_task_by_id(session, user_id, task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return {"task": task}


@router.delete("/tasks/{task_id}", summary="Удаление задачи", description="Эндпоинт для удаления задачи пользователя.")
async def delete_task(task_id: int, user_id: int, session: AsyncSession = Depends(db_helper.session_dependency), credentials: JwtAuthorizationCredentials = Security(access_security)):
    await crud.delete_user_task(session, user_id, task_id)
    return {"message": "Задача успешно удалена"}