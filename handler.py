from storefront_monitor.store import list_inventory
from storefront_monitor.cache import create_client, get_saved, batch_save

def handler(event, context):
    inv = list_inventory()
    client = create_client()

    await batch_save(client, '-storefrontmonitor-current', inv)
    
    return None