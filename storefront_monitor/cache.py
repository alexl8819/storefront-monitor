from json import dumps
from upstash_redis.asyncio import Redis

def create_client() -> Redis:
    return Redis.from_env(allow_telemetry=False)

async def batch_save(client, key, item) -> None: 
    await client.set(key, dumps(item))

async def get_saved(client, key) -> str:
    saved_item = await client.get(key)
    return saved_item
    