from operator import and_

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from trial.application import Pair, Quote, QuoteRepo

from .alch_model import QuoteModel


class AlchemyQuoteRepo(QuoteRepo):
    def __init__(self, eng: AsyncEngine):
        self._engine = eng

    async def get_last_quote(self, pair: Pair) -> Quote:
        async with self._engine.begin() as conn:
            result = await conn.execute(
                select(
                    QuoteModel.c.pair,
                    QuoteModel.c.ts,
                    QuoteModel.c.rate,
                )
                .where(QuoteModel.c.pair == pair)
                .order_by(QuoteModel.c.quote_id.desc())
            )
            result = result.fetchone()
            if result is None:
                raise self.NotFound(f"quote for {pair} not found")
        return Quote(**result._mapping)

    async def save_quote(self, quote: Quote):
        async with self._engine.begin() as conn:
            result = await conn.execute(
                select(QuoteModel.c.quote_id).where(
                    and_(QuoteModel.c.ts == quote.ts, QuoteModel.c.pair == quote.pair)
                )
            )
            result = result.fetchone()
            if result is not None:
                result = await conn.execute(
                    QuoteModel.update()
                    .where(QuoteModel.c.quote_id == result._mapping["quote_id"])
                    .values(**quote.dict())
                )
            else:
                result = await conn.execute(QuoteModel.insert().values(**quote.dict()))
