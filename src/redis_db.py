import redis.asyncio as redis
from config import settings

import pickle
from typing import Dict, Union


class RedisApi:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    @staticmethod
    def make_redis_key(namespace: str, key: str) -> str:
        """
        Создание ключа для redis, используя namespace и токен.
        """
        return f'{namespace}:{key}'

    def convert(self, data: Union[dict, tuple, bytes]):
        """
        Функция декодирования данных из хеш-таблиц редиса, которые приходят в виде байтов или pickle объектов.
        """

        if isinstance(data, bytes):
            try:
                value = pickle.loads(data)
            except (KeyError, pickle.UnpicklingError):
                value = data.decode()
            return value

        if isinstance(data, dict):
            return dict(map(self.convert, data.items()))

        if isinstance(data, tuple):
            return map(self.convert, data)

        return data

    async def _redis_expire(self, redis_key: str, expire_time: int | None) -> None:
        if expire_time:
            await self.redis.expire(redis_key, expire_time)

    async def hset(self, namespace: str, key: str, map_: dict, expire_time: int | None = None) -> None:
        redis_key = self.make_redis_key(namespace, key)
        await self.redis.hset(redis_key, mapping=map_)
        await self._redis_expire(redis_key, expire_time)

    async def hgetall(self, name: str) -> Dict[str, str | int]:
        return self.convert(await self.redis.hgetall(name))

    async def exists(self, name: str) -> bool:
        return await self.redis.exists(name)


redis_api = RedisApi()
