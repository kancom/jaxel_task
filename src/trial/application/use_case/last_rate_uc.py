from loguru import logger

from ..domain.model import Quote
from ..foundation import Pair
from ..repository.quote_repo import QuoteRepo


class GetLastRateUseCase:
    def __init__(self, quote_repo: QuoteRepo) -> None:
        self._quote_repo = quote_repo

    async def excecute(self, pair: Pair) -> Quote:
        try:
            quote = await self._quote_repo.get_last_quote(pair=pair)
        except self._quote_repo.NotFound as ex:
            logger.error(f"Can't get last quote for {pair} {ex}")
            raise
        return quote
