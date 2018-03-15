from __future__ import print_function # Python 2/3 compatibility
import os, sys
import json
import asyncio
import websockets
import re
import boto3
import decimal

debug=False

dynamodb = boto3.resource('dynamodb',region_name='us-east-2') 
table = dynamodb.Table(sys.argv[1]) # exemple btc_candles

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

async def get_candles(log_file):
	async with websockets.connect('wss://api.bitfinex.com/ws/2') as websocket:
		msg = json.dumps({'event': 'subscribe', 'channel': 'candles', 'key': sys.argv[2]}) # exemple tBTCUSD
		await websocket.send(msg)
		print("> {}".format(msg), file=log_file)

		info = await websocket.recv()
		print("< {}".format(info), file=log_file)

		event = await websocket.recv()
		print("< {}".format(event), file=log_file)

		while True:
			response = await websocket.recv()
			parsed_response = re.split(',|\[|\]', response)
			if(len(parsed_response) == 11):
				if(debug):
					print(parsed_response, file=log_file, flush=True)
				response = table.put_item(
				   Item={
				        'mts': parsed_response[3],
				        'open': parsed_response[4],
				        'close': parsed_response[5],
				        'high': parsed_response[6],
				        'low': parsed_response[7],
				        'volume': parsed_response[8]
				    }
				)

if len(sys.argv) < 3:
	print("Wrong number of arguments : 2 or 3 expected")
	print("[USAGE] python websocket-client-candles.py <db_table_name> <currency symbol> <debug=False>")
	print("[EXEMPLE] python websocket-client-candles.py btc_candles trade:15m:tBTCUSD True")

else:
	if(len(sys.argv) == 4):
		debug=sys.argv[3]

	with open('websocket-logs.txt', 'w') as f:
		print("db table name : ", sys.argv[1], file=f)
		print("websocket channel to subscribe : candles", file=f)
		print("currency symbol: ", sys.argv[2], file=f)
		if(len(sys.argv) == 4):
			debug=sys.argv[3]
		print("debug: ", debug, file=f)

		asyncio.get_event_loop().run_until_complete(get_candles(f))