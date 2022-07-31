import asyncio

from fastapi import FastAPI
from loguru import logger

from trial.api.http_api import router
from trial.application import SaveQuoteUseCase
from trial.infrastructure import KafkaBusAdapter, KafkaBusConsumer
from trial.settings import KafkaSettings

from .wiring import init_db

kafka_settings = KafkaSettings()

logger.debug(f"Starting with {kafka_settings.dict()}")


async def task(uc: SaveQuoteUseCase):
    await uc.excecute()


def prepare_uc():
    quote_repo = init_db()
    adapter = KafkaBusAdapter()
    bus_consumer = KafkaBusConsumer(
        adapter=adapter,
        bootstrap_servers=kafka_settings.bootstrap_servers,
        topic=kafka_settings.topic,
    )
    uc = SaveQuoteUseCase(quote_repo=quote_repo, bus_consumer=bus_consumer)
    asyncio.create_task(task(uc))


def prepare_app():
    app = FastAPI()
    app.on_event("startup")(prepare_uc)
    app.include_router(router)
    return app


app = prepare_app()
