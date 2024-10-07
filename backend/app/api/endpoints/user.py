from fastapi import APIRouter, Depends, HTTPException, status, Response, Security
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from api.endpoints import access_security
from api.schemas import UserCreateSchema
from database.db_helper import db_helper
from database.requests.user import crud

router = APIRouter()


@router.post("/register", summary="Регистрация пользователя", description="Эндпоинт для регистрации нового пользователя.")
async def register_user(user_data: UserCreateSchema, session: AsyncSession = Depends(db_helper.session_dependency)):
    user = await crud.get_user_by_email(session, user_data.email)
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Пользователь уже существует")
    new_user = await crud.register_user(session, user_data.dict())

    return {"message": "Пользователь успешно зарегистрирован", "user": new_user}


@router.get("/login", summary="Авторизация пользователя", description="Эндпоинт для авторизации пользователя по email.")
async def login_user(email: EmailStr, response: Response, session: AsyncSession = Depends(db_helper.session_dependency)):
    user = await crud.get_user_by_email(session, email)

    access_token = access_security.create_access_token(subject={'user_id': user.id})
    access_security.set_access_cookie(response, access_token)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return {"message": "Успешная авторизация", "access_token": access_token, "user": user}