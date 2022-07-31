from typing import AsyncGenerator

from aiokafka import AIOKafkaConsumer
from loguru import logger
from trial.application import BusAdapter, BusConsumer


class KafkaBusConsumer(BusConsumer):
    def __init__(self, adapter: BusAdapter, bootstrap_servers: str, topic: str) -> None:
        self._adapter = adapter
        self._started = False
        self._topic = topic
        self._bootstrap_servers = bootstrap_servers

    async def _start(self):
        self._consumer = AIOKafkaConsumer(
            self._topic, bootstrap_servers=self._bootstrap_servers
        )
        await self._consumer.start()
        self._started = True

    async def consume_messages(self) -> AsyncGenerator:
        if not self._started:
            await self._start()
        logger.debug(f"Consumer started {self._consumer}")
        async for msg in self._consumer:
            quote = self._adapter.deserialize_quote(msg)
            logger.debug(f"{quote} received")
            yield quote
