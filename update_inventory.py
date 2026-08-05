import asyncio
from os import getenv
from datetime import datetime

from storefront_monitor.store import list_inventory
from storefront_monitor.cache import batch_save

async def run_update():
    await batch_save(getenv('inventory_key'), dict({
        'last_updated': datetime.now().isoformat(),
        'items': list_inventory()
    }))

def handler(event, context):
    asyncio.run(run_update())