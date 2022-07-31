import abc
from typing import AsyncGenerator

from ..domain.model import Quote


class BusProducer(metaclass=abc.ABCMeta):
    class BusError(Exception):
        pass

    @abc.abstractmethod
    async def push_quote(self, quote: Quote):
        pass


class BusConsumer(metaclass=abc.ABCMeta):
    class BusError(Exception):
        pass

    @abc.abstractmethod
    async def consume_messages(self) -> AsyncGenerator:
        pass
