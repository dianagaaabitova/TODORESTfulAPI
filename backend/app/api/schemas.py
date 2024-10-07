from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    username: str = Field(..., description="Имя пользователя", min_length=3, max_length=50)


class TaskCreateSchema(BaseModel):
    title: str = Field(..., description="Название задачи", min_length=1, max_length=255)
    user_id: int = Field(..., description="Идентификатор пользователя")


class JobCreateSchema(BaseModel):
    task_id: int = Field(..., description="Идентификатор задачи")
    title: str = Field(..., description="Название работы", min_length=1, max_length=255)