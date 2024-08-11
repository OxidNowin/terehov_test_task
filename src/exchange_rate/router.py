from fastapi import APIRouter

from schemas import CurrencyRate
from consts import redis_namespace
from redis_db import redis_api

from datetime import date

router = APIRouter(
    prefix="/exchange_rate",
    tags=["Exchange rate"],
)


@router.get("/{currency}")
async def get_exchange_rate(currency: str) -> CurrencyRate | None:
    today = date.today().strftime("%d.%m.%Y")
    name = f'{redis_namespace}:{today}:{currency.upper()}'
    data = await redis_api.hgetall(name)
    if not data:
        return
    return CurrencyRate(**data)
