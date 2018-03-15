from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

client = boto3.client('dynamodb')

response = client.scan(
    TableName='btc_candles_5m',
)

with open("btc_candles_5m.txt", "w") as outfile:
    json.dump(response, outfile)

print(response)