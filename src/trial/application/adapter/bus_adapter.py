import abc
from typing import Generic, TypeVar

from ..domain.model import Quote

T = TypeVar("T")


class BusAdapter(Generic[T], metaclass=abc.ABCMeta):
    class AdapterException(Exception):
        pass

    @abc.abstractmethod
    def serialize_quote(self, quote: Quote) -> T:
        pass

    @abc.abstractmethod
    def deserialize_quote(self, raw: T) -> Quote:
        pass
