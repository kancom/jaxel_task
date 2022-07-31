from loguru import logger

from ..foundation import Pair
from ..repository.bus_repo import BusProducer
from ..repository.quote_provider_repo import QuoteProviderRepo


class PollUseCase:
    def __init__(
        self,
        pair: Pair,
        quote_provider_repo: QuoteProviderRepo,
        bus_producer: BusProducer,
    ) -> None:
        self._pair = pair
        self._quote_provider = quote_provider_repo
        self._bus_producer = bus_producer

    async def excecute(self):
        quote = await self._quote_provider.get(pair=self._pair)
        logger.debug(quote)
        await self._bus_producer.push_quote(quote)
