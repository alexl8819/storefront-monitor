from json import dumps
from upstash_redis.asyncio import Redis

async def batch_save(key, item) -> None:
    async with Redis.from_env(allow_telemetry=False) as client:
        await client.set(key, dumps(item))

async def get_saved(key) -> str:
    async with Redis.from_env(allow_telemetry=False) as client:
        saved_item = await client.get(key)
        return saved_item

