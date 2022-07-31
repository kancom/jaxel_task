import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

from trial.application import PollUseCase
from trial.infrastructure import (GarantexQuoteProviderAdapter,
                                  GarantexQuoteProviderRepo, KafkaBusAdapter,
                                  KafkaBusProducer)
from trial.settings import PollSettings


def poller():
    settings = PollSettings()
    logger.debug(f"Starting with {settings.dict()}")
    scheduler = AsyncIOScheduler()
    garantex_adapter = GarantexQuoteProviderAdapter()
    quote_p_repo = GarantexQuoteProviderRepo(adapter=garantex_adapter)
    kafka_adapter = KafkaBusAdapter()
    bus_producer = KafkaBusProducer(
        adapter=kafka_adapter,
        bootstrap_servers=settings.bootstrap_servers,
        topic=settings.topic,
    )
    uc = PollUseCase(
        pair=settings.pair, quote_provider_repo=quote_p_repo, bus_producer=bus_producer
    )
    scheduler.add_job(uc.excecute, "interval", seconds=settings.interval)
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    poller()
