from asyncio import current_task

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncSession

from config import config_dict


class DatabaseHelper:
    def __init__(self):
        self.engine = create_async_engine(
            config_dict.db.construct_sqlalchemy_url(),  # + '?ssl=require',
            echo=False
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self.scopefunc = current_task  # Using current_task as the scope function for async_scoped_session

    def get_session(self):
        # Creates a scoped session. Note that async_scoped_session is meant for scenarios
        # where the session's lifecycle is tied to some scope (like an async web request).
        return async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=self.scopefunc
        )

    async def session_dependency(self) -> AsyncSession:
        # Directly use the scoped session without async with
        # The session's lifecycle is managed by the scope (e.g., a web request)
        session = self.get_session()
        try:
            yield session
        finally:
            await session.close()  # Correctly close the session


db_helper = DatabaseHelper()
