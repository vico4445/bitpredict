
# coding: utf-8

# In[67]:

import urllib.request, urllib.error, urllib.parse
import time
import json
from pymongo import MongoClient
import sys
import requests


# In[68]:
#http://data.btcchina.com/data/historydata?since=1407942004&limit=5000&sincetype=time
api = 'https://api.bitfinex.com/v1'
symbol = sys.argv[1]
limit = 1000

client = MongoClient()
db = client['bitmicro']
ltc_trades = db[symbol+'_trades']


# In[69]:

def format_trade(trade):
    '''
    Formats trade data
    '''
    if all(key in trade for key in ('tid', 'amount', 'price', 'timestamp')):
        trade['_id'] = trade.pop('tid')
        trade['amount'] = float(trade['amount'])
        trade['price'] = float(trade['price'])
        trade['timestamp'] = float(trade['timestamp'])

    return trade


def get_json(url):
    '''
    Gets json from the API
    '''
    #resp = urllib.request.urlopen(url)
    #str_response = resp.read().decode('utf-8')
    resp = requests.get(url=url)
    return resp.json() , resp.status_code
    #return json.load(str_response, object_hook=format_trade), resp.getcode()


# In[71]:

print('Running...')
last_timestamp = 0
while True:
    start = time.time()
    url = '{0}/trades/{1}usd?timestamp={2}&limit_trades={3}'        .format(api, symbol, last_timestamp, limit)
    try:
        trades, code = get_json(url)
    except Exception as e:
        print(e)
    else:
        if code != 200:
            print(code)
            time.sleep(20)
        else:
            for trade in trades:
                ltc_trades.update_one({'_id': trade['tid']},
                                      {'$setOnInsert': trade}, upsert=True)
            if(len(trades) > 0):
                last_timestamp = trades[0]['timestamp'] - 5
            time_delta = time.time()-start

            if time_delta < 5:
                time.sleep(5-time_delta)