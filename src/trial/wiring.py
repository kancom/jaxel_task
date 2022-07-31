from typing import cast

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from trial.infrastructure import AlchemyQuoteRepo
from trial.settings import PresentationSettings

present_settings = PresentationSettings()

logger.debug(f"Starting with {present_settings.dict()}")


def get_async_db_engine(dsn: str) -> AsyncEngine:
    engine = cast(
        AsyncEngine,
        create_async_engine(dsn, echo=True, pool_pre_ping=True),
    )
    return engine


def init_db():
    eng = get_async_db_engine(present_settings.db_dsn)
    return AlchemyQuoteRepo(eng)
