from trial.application import Pair, Quote, QuoteRepo

from .tort_model import QuoteModel


class TortoiseQuoteRepo(QuoteRepo):
    async def get_last_quote(self, pair: Pair) -> Quote:
        raw_quote = (
            await QuoteModel.all().filter(pair=pair).order_by("-quote_id").first()
        )
        if raw_quote is None:
            raise self.NotFound("no quotes found")
        return Quote(pair=raw_quote.pair, rate=raw_quote.rate, ts=raw_quote.ts)

    async def save_quote(self, quote: Quote):
        await QuoteModel.create(**quote.dict())
