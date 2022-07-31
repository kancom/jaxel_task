import abc

from ..domain.model import Quote
from ..foundation import Pair


class QuoteRepo(metaclass=abc.ABCMeta):
    class NotFound(Exception):
        pass

    @abc.abstractmethod
    async def save_quote(self, quote: Quote):
        pass

    @abc.abstractmethod
    async def get_last_quote(self, pair: Pair) -> Quote:
        pass
