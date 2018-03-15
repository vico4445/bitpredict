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
table = dynamodb.Table(sys.argv[1])

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

async def get_trades():
	async with websockets.connect('wss://api.bitfinex.com/ws/2') as websocket:
		msg = json.dumps({'event': 'subscribe', 'channel': sys.argv[2], 'symbol': sys.argv[3]})
		await websocket.send(msg)
		print("> {}".format(msg))

		info = await websocket.recv()
		print("< {}".format(info))

		event = await websocket.recv()
		print("< {}".format(event))

		while True:
			response = await websocket.recv()
			parsed_response = re.split(',|\[|\]', response)
			if(len(parsed_response) == 10):
				if(parsed_response[2] == "\"tu\""):
					if(debug):
						print(parsed_response)
					response = table.put_item(
					   Item={
					        '_id': parsed_response[5],
					        'amount': decimal.Decimal(parsed_response[6]),
					        'price': parsed_response[7]
					    }
					)
if len(sys.argv) < 4:
	print("Wrong number of arguments : 3 or 4 expected")
	print("[USAGE] python websocket-client.py <db_table_name> <websocket channel> <currency symbol> <debug=False>")
	print("[EXEMPLE] python websocket-client.py btc_trades trades tBTCUSD True")

else:
	print("db table name : ", sys.argv[1])
	print("websocket channel to subscribe : ", sys.argv[2])
	print("currency symbol: ", sys.argv[3])
	if(len(sys.argv) == 5):
		debug=sys.argv[4]
	print("debug: ", debug)

	asyncio.get_event_loop().run_until_complete(get_trades())