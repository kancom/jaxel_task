from datetime import datetime
from typing import List

from trial.application import Quote, QuoteProviderAdapter


class GarantexQuoteProviderAdapter(QuoteProviderAdapter):
    def decode_quote(self, raw: List) -> List[Quote]:
        result = []
        try:
            for raw_quote in raw:
                quote = Quote(
                    pair=raw_quote["market"].upper(),
                    ts=raw_quote["created_at"],
                    rate=raw_quote["price"],
                )
                quote.ts = datetime.fromtimestamp(quote.ts.timestamp())
                result.append(quote)

        except Exception as ex:
            raise self.AdapterException(f"decoding error") from ex
        return result
