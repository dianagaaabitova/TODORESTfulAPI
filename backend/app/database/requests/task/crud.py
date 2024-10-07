from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Task

async def get_user_tasks(session: AsyncSession, user_id: int):
    async with session.begin():
        result = await session.execute(select(Task).filter_by(user_id=user_id))
        return result.scalars().all()

async def create_user_task(session: AsyncSession, user_id: int, task_data: dict):
    task_data["user_id"] = user_id
    task = Task(**task_data)
    session.add(task)

    await session.commit()
    return task

async def get_task_by_id(session: AsyncSession, user_id: int, task_id: int):
    async with session.begin():
        result = await session.execute(select(Task).filter_by(id=task_id, user_id=user_id))
        return result.scalars().first()

async def delete_user_task(session: AsyncSession, user_id: int, task_id: int) -> None:
    await session.execute(delete(Task).where(Task.id == task_id, Task.user_id == user_id))
    await session.commit()