from typing import List, Optional

import aiohttp
from trial.application import (Pair, Quote, QuoteProviderAdapter,
                               QuoteProviderRepo)


class GarantexQuoteProviderRepo(QuoteProviderRepo):
    base_url = "https://garantex.io/api/v2/"
    endpoint_map = {QuoteProviderRepo.Endpoint.TRADES: "trades"}

    def __init__(self, adapter: QuoteProviderAdapter) -> None:
        self._adapter = adapter
        self._client_session_method = aiohttp.ClientSession

    async def _query(
        self, endpoint: QuoteProviderRepo.Endpoint, query_data: Optional[dict] = None
    ) -> List:
        url = f"{self.base_url}{self.endpoint_map[endpoint]}"
        async with self._client_session_method() as session:
            async with session.get(url, params=query_data) as resp:
                if 200 > resp.status or resp.status > 299:
                    raise self.NotFound(
                        f"unexpcted response {resp.status} {url}, {query_data}, {resp.text}"
                    )
                return await resp.json()

    async def get(self, pair=Pair) -> Quote:
        query_data = {"market": pair.lower(), "limit": 1}
        raw_quote = await self._query(self.Endpoint.TRADES, query_data=query_data)
        quote = self._adapter.decode_quote(raw_quote)[0]
        return quote
