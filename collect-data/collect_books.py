
# coding: utf-8

# In[5]:

import urllib.request, urllib.error, urllib.parse
import time
import json
from pymongo import MongoClient
import sys
import requests

api = 'https://api.bitfinex.com/v1'
symbol = sys.argv[1]
limit = 25
book_url = '{0}/book/{1}usd?limit_bids={2}&limit_asks={2}'    .format(api, symbol, limit)

client = MongoClient()
db = client['bitmicro']
ltc_books = db[symbol+'_books']


def format_book_entry(entry):
    '''
    Converts book data to float
    '''
    if all(key in entry for key in ('amount', 'price', 'timestamp')):
        entry['amount'] = float(entry['amount'])
        entry['price'] = float(entry['price'])
        entry['timestamp'] = float(entry['timestamp'])
    return entry


def get_json(url):
    '''
    Gets json from the API
    '''
    #resp = urllib.request.urlopen(url)
    #return json.load(resp, object_hook=format_book_entry), resp.getcode()
    resp = requests.get(url=url)
    return resp.json() , resp.status_code


print('Running...')
while True:
    start = time.time()
    try:
        book, code = get_json(book_url)
    except Exception as e:
        print(e)
    else:
        if code != 200:
            print(code)
            time.sleep(20)
        else:
            book['_id'] = time.time()
            ltc_books.insert_one(book)
            time_delta = time.time()-start

            if time_delta < 5:
                time.sleep(5-time_delta)

