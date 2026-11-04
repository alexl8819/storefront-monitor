from os import getenv
from datetime import datetime, timezone
import datetime as dt
import asyncio
from secure_dotenv import load_dotenv

from storefront_monitor.cache import batch_save

from bs4 import BeautifulSoup
from ebaysdk.trading import Connection as Trading

load_dotenv()

MAX_ITEMS_PER_PAGE = 200
MAX_FUTURE_DAYS_DELTA = 90

def _clean_listing_formatting(text):
    return BeautifulSoup(text, 'html.parser').get_text('\n', strip=True)

def _parse_item(item) -> dict:
    item = item['Item']

    reduced_item = {}
    reduced_item['title'] = item['Title']
    reduced_item['description'] = _clean_listing_formatting(item['Description'])
    reduced_item['status'] = item['SellingStatus']['ListingStatus']
    reduced_item['quantity'] = int(item['Quantity']) or 1
    reduced_item['quantity_sold'] = int(item['SellingStatus']['QuantitySold']) or 0
    reduced_item['category_sku'] = item['SKU']
    reduced_item['price'] = float(item['ListingDetails']['ConvertedStartPrice']['value']) or 0.00
    reduced_item['condition'] = item['ConditionDisplayName']
    reduced_item['condition_description'] = item['ConditionDescription'] if 'ConditionDescription' in item else 'N/A'
    reduced_item['listing_url'] = item['ListingDetails']['ViewItemURL']
    reduced_item['time_left'] = item['TimeLeft']
    reduced_item['main_screenshot'] = item['PictureDetails']['PictureURL']
    reduced_item['returns_policy'] = item['ReturnPolicy']

    return reduced_item

def list_inventory(start_time=datetime.today(), page = 1, inv = []) -> [dict]:
    end_time = dt.timedelta(days=MAX_FUTURE_DAYS_DELTA) + start_time
    
    api = Trading(
        domain='api.ebay.com',
        appid=getenv('appid'),
        certid=getenv('certid'),
        devid=getenv('devid'),
        token=getenv('token'),
        config_file=None
    )
    response = api.execute('GetSellerList', { # Assume 200 listing per page
        'EndTimeFrom': start_time.isoformat(),
        'EndTimeTo': end_time.isoformat(),
        'GranularityLevel': 'Coarse',
        'Pagination': {
            'EntriesPerPage': MAX_ITEMS_PER_PAGE,
            'PageNumber': page
        }
    })

    s_list = response.dict()
    items = s_list['ItemArray']['Item']

    for item in items:
        item_response = api.execute('GetItem', {
            'ItemID': item['ItemID'],
            'DetailLevel': 'ReturnAll',
            'IncludeItemSpecifics': True
        })

        inv.append(_parse_item(item_response.dict()))

    if len(items) >= MAX_ITEMS_PER_PAGE:
        return list_inventory(start_time, page + 1, inv)

    return inv

async def main():
    await batch_save(getenv('inventory_key'), dict({
        'last_updated': datetime.now().isoformat(),
        'items': list_inventory()
    }))
    print('Updated inventory')

if __name__ == "__main__":
    asyncio.run(main())