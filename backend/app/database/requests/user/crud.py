from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import User


async def register_user(session: AsyncSession, user_data: dict):
    user = User(**user_data)
    session.add(user)

    await session.commit()
    return user

async def get_user_by_email(session: AsyncSession, email: str):
    async with session.begin():
        result = await session.execute(select(User).filter_by(email=email))
        return result.scalars().first()

async def get_user(session: AsyncSession, id: int):
    async with session.begin():
        result = await session.execute(select(User).filter_by(id=id))
        return result.scalars().first()

async def delete_user(session: AsyncSession, id: int) -> None:
    await session.execute(delete(User).where(User.id == id))
    await session.commit()