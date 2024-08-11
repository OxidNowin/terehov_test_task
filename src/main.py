from fastapi import FastAPI

from exchange_rate.utils import set_currency_rates
from exchange_rate.router import router as exchange_rates_router


app = FastAPI()


@app.on_event("startup")
async def startup():
    await set_currency_rates()


app.include_router(exchange_rates_router)
