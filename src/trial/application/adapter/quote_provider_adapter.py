import abc
from typing import List

from ..domain.model import Quote


class QuoteProviderAdapter(metaclass=abc.ABCMeta):
    class AdapterException(Exception):
        pass

    @abc.abstractmethod
    def decode_quote(self, raw: List) -> List[Quote]:
        pass
