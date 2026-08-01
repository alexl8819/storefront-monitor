import asyncio

from storefront_monitor.store import list_inventory
from storefront_monitor.cache import batch_save

async def run_update():
    await batch_save('-storefrontmonitor-current', list_inventory())

def handler(event, context):
    return asyncio.run(run_update())