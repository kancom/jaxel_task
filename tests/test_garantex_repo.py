import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from trial.application import Pair
from trial.infrastructure import (GarantexQuoteProviderAdapter,
                                  GarantexQuoteProviderRepo)


def proper_resp():
    return [
        {
            "id": 34786,
            "price": "68.8",
            "volume": "757.51",
            "funds": "52116.84",
            "market": "usdtrub",
            "created_at": "2020-04-25T12:54:22+03:00",
        },
    ]


def broken_resp():
    return [
        {
            "id": 34786,
            "volume": "757.51",
            "funds": "52116.84",
            "market": "usdtrub",
            "created_at": "2020-04-25T12:54:22+03:00",
        },
    ]


def garantex_get(*args, params, **kwargs):
    if params["market"] == "usdtrub":
        get_mock = AsyncMock()
        get_mock.__aenter__.return_value.status = 200
        get_mock.__aenter__.return_value.json.return_value = proper_resp()
        return get_mock
    elif params["market"] == "usdtrub_b":
        get_mock = AsyncMock()
        get_mock.__aenter__.return_value.status = 200
        get_mock.__aenter__.return_value.json.return_value = broken_resp()
        return get_mock
    else:
        raise GarantexQuoteProviderRepo.NotFound()


@pytest.fixture
def repo():
    cli_sess_mock = MagicMock(name="cli_sess_mock")
    with patch(
        "aiohttp.ClientSession",
        return_value=cli_sess_mock,
        name="CliSessMock",
    ):
        sess_mock = MagicMock(name="sess_mock")
        cli_sess_mock.__aenter__.return_value = sess_mock
        sess_mock.get.side_effect = garantex_get

        adapter = GarantexQuoteProviderAdapter()
        repo = GarantexQuoteProviderRepo(adapter)
    return repo


@pytest.mark.asyncio
async def test_get(repo: GarantexQuoteProviderRepo, pair: Pair):
    quote = await repo.get(pair)
    assert quote.pair == pair
    assert quote.rate > 0


@pytest.mark.asyncio
async def test_get_fail(repo: GarantexQuoteProviderRepo):
    non_existing_pair = Pair("USDTRBB")
    with pytest.raises(GarantexQuoteProviderRepo.NotFound):
        await repo.get(non_existing_pair)


@pytest.mark.asyncio
async def test_get_fail_adapter(repo: GarantexQuoteProviderRepo):
    non_existing_pair = Pair("USDTRUB_B")
    with pytest.raises(GarantexQuoteProviderAdapter.AdapterException):
        await repo.get(non_existing_pair)
