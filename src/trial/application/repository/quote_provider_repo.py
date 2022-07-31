import abc
from enum import IntEnum

from ..domain.model import Quote
from ..foundation import Pair


class QuoteProviderRepo(metaclass=abc.ABCMeta):
    class NotFound(Exception):
        pass

    class Endpoint(IntEnum):
        TRADES = 1

    @abc.abstractmethod
    async def get(self, pair=Pair) -> Quote:
        pass
