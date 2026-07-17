import logging
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.app.core.config import settings
from backend.app.models.leads import Base

logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self._engine = None
        self._sessionmaker = None
        self.db_url = settings.DATABASE_URL

    async def close(self):
        if self._engine is None:
            return
        await self._engine.dispose()
        self._engine = None
        self._sessionmaker = None
        logger.info("SQlite successfully closed")

    @asynccontextmanager
    async def session_scope(self):
        if self._sessionmaker is None:
            logger.error("SQlite sessionmaker not initialized")
            raise IOError("SQlite sessionmaker not initialized")

        session = self._sessionmaker()
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Error in background SQlite transaction: {e}")
            raise e
        finally:
            await session.close()

    async def get_session(self):
        if self._sessionmaker is None:
            logger.error("SQlite initiated with an error")
            raise IOError("SQlite initiated with an error")
        async with self._sessionmaker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                logger.error(f"Error SQlite: {e}")
                raise e
            finally:
                await session.close()

    async def init_db(self):
        if self._engine is None:
            self._engine = create_async_engine(settings.DATABASE_URL, echo=False)
            self._sessionmaker = async_sessionmaker(
                bind=self._engine,
                class_=AsyncSession,
                expire_on_commit=False
            )
            logger.info(f"SQlite successfully initialized")
            async with self._engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")

db = Database()
