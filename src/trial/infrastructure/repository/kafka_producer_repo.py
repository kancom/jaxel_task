from aiokafka import AIOKafkaProducer
from loguru import logger
from trial.application import BusAdapter, BusProducer, Quote


class KafkaBusProducer(BusProducer):
    def __init__(self, adapter: BusAdapter, bootstrap_servers: str, topic: str) -> None:
        self._adapter = adapter
        self._started = False
        self._topic = topic
        self._bootstrap_servers = bootstrap_servers

    async def _start(self):
        self._producer = AIOKafkaProducer(bootstrap_servers=self._bootstrap_servers)
        await self._producer.start()
        self._started = True

    async def push_quote(self, quote: Quote):
        if not self._started:
            await self._start()
        raw_msg = self._adapter.serialize_quote(quote)
        await self._producer.send_and_wait(self._topic, raw_msg)
        logger.debug(f"{quote} sent")
