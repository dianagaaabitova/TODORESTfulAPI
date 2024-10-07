from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Job, Task

async def create_job_for_task(session: AsyncSession, user_id: int, task_id: int, job_data: dict):
    task = await session.get(Task, task_id)
    if not task or task.user_id != user_id:
        return None
    job_data["task_id"] = task_id
    job = Job(**job_data)
    session.add(job)
    await session.commit()
    return job

async def mark_job_as_completed(session: AsyncSession, user_id: int, job_id: int):
    result = await session.execute(select(Job).filter_by(id=job_id))
    job = result.scalars().first()
    if not job:
        return None
    task = await session.get(Task, job.task_id)
    if not task or task.user_id != user_id:
        return None
    await session.execute(update(Job).where(Job.id == job_id).values(is_completed=True))
    await session.commit()
    return job