from exchange_rate.utils import set_currency_rates

from src.tasks.celeryconfig import app


@app.task
async def fetch_currency_rates():
    await set_currency_rates()
