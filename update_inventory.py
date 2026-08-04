import asyncio
from os import getenv

from storefront_monitor.store import list_inventory
from storefront_monitor.cache import batch_save

async def run_update():
    await batch_save(getenv('inventory_key'), list_inventory())

def handler(event, context):
    asyncio.run(run_update())