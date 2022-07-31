import json

from aiokafka import ConsumerRecord
from loguru import logger
from trial.application import BusAdapter, Quote


class KafkaBusAdapter(BusAdapter[bytes]):
    def serialize_quote(self, quote: Quote) -> bytes:
        return quote.json().encode("utf-8")

    def deserialize_quote(self, raw: ConsumerRecord) -> Quote:
        logger.debug(f"new msg {raw}")
        return Quote(**json.loads(raw.value.decode("utf-8")))
