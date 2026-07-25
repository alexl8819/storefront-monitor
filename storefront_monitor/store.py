from os import getenv
from datetime import datetime, timezone
import datetime as dt
import asyncio
from secure_dotenv import load_dotenv

from storefront_monitor.cache import create_client, batch_save, get_saved

from ebaysdk.trading import Connection as Trading

load_dotenv()

def _parse_item(item) -> dict:
    item = item['Item']

    reduced_item = {}
    reduced_item['title'] = item['Title']
    reduced_item['quantity'] = int(item['Quantity']) or 1
    reduced_item['price'] = item['ListingDetails']['ConvertedStartPrice']['value']
    reduced_item['listing_url'] = item['ListingDetails']['ViewItemURL']
    reduced_item['main_screenshot'] = item['PictureDetails']['PictureURL']
    reduced_item['returns_policy'] = item['ReturnPolicy']

    return reduced_item

def list_inventory(start_time=datetime.today()) -> [dict]:
    end_time = dt.timedelta(days=30) + start_time
    
    api = Trading(
        domain='api.ebay.com',
        appid=getenv('appid'),
        certid=getenv('certid'),
        devid=getenv('devid'),
        token=getenv('token'),
        config_file=None
    )
    response = api.execute('GetSellerList', {
        'EndTimeFrom': start_time.isoformat(),
        'EndTimeTo': end_time.isoformat()
    })
    s_list = response.dict()

    items = s_list['ItemArray']
    inv = []

    if isinstance(items, dict):
        item_response = api.execute('GetItem', {
            'ItemID': items['Item']['ItemID']
        })
        inv.append(_parse_item(item_response.dict()))
    else:
        for item in items:
            i = items[item]
            for it in i:
                item_response = api.execute('GetItem', { 
                    'ItemID': it['ItemID']
                })
                inv.append(_parse_item(item_response.dict()))
    return inv

async def main():
    inv = list_inventory()
    client = create_client()

    if len(inv) == 0:
        inv = await get_saved(client, '-storefrontmonitor-current')
        print(inv)
        print('No items found in batch.')

    await batch_save(client, '-storefrontmonitor-current', inv)
    print('Updated inventory')

if __name__ == "__main__":
    asyncio.run(main())