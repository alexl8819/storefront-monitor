from datetime import datetime, timezone
import datetime as dt

from ebaysdk.trading import Connection as Trading

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

def list_inventory(start_time=datetime.today()) -> dict or [dict]:
    end_time = dt.timedelta(days=30) + start_time
    
    api = Trading(config_file='./ebay-credentials.yaml')
    response = api.execute('GetSellerList', {
        'EndTimeFrom': start_time.isoformat(),
        'EndTimeTo': end_time.isoformat()
    })
    d = response.dict()
    #print(d)

    items = d['ItemArray']

    if isinstance(items, dict):
        item_response = api.execute('GetItem', {
            'ItemID': items['Item']['ItemID']
        })
        return _parse_item(item_response.dict())
    else:
        inv = []
        for item in items:
            i = items[item]
            for it in i:
                item_response = api.execute('GetItem', { 
                    'ItemID': it['ItemID']
                })
                inv.append(_parse_item(item_response.dict()))
        return inv

print(list_inventory())