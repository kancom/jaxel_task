from ..domain.model import Quote
from ..repository.bus_repo import BusConsumer
from ..repository.quote_repo import QuoteRepo


class SaveQuoteUseCase:
    def __init__(self, quote_repo: QuoteRepo, bus_consumer: BusConsumer) -> None:
        self._quote_repo = quote_repo
        self._consumer = bus_consumer

    async def excecute(self):
        async for quote in self._consumer.consume_messages():
            await self._quote_repo.save_quote(quote)
