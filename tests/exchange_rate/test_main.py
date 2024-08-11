from src.exchange_rate.utils import get_currency_rates, set_currency_rates
from src.redis_db import redis_api

import pytest
from datetime import date


@pytest.mark.asyncio
async def test_get_currency_rates():
    data = await get_currency_rates()
    assert data is not None


@pytest.mark.asyncio
async def test_get_currency_rates():
    await set_currency_rates()
    today = date.today().strftime("%d.%m.%Y")
    name = f'exchange_rates:{today}:USD'
    data = await redis_api.hgetall(name)
    assert data is not None
