from redis_db import redis_api
from consts import redis_namespace, redis_expire_time, currency_rate_url

from typing import Dict

import aiohttp
import xmltodict


async def get_currency_rates() -> Dict[str, Dict[str, str | list[Dict[str, str]]]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(currency_rate_url) as resp:
            data = await resp.text()
            data_dict = xmltodict.parse(data)
    return data_dict


async def set_currency_rates() -> None:
    data = await get_currency_rates()
    val_curs = data['ValCurs']
    date = val_curs['@Date']

    if await redis_api.exists(f'{redis_namespace}:{date}'):
        return

    valute = val_curs['Valute']
    for val in valute:
        val_id = val['@ID']
        val.pop('@ID')
        val['Id'] = val_id
        await redis_api.hset(f'{redis_namespace}:{date}', val['CharCode'], val, expire_time=redis_expire_time)
