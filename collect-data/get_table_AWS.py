import boto3
import json

client = boto3.client('dynamodb')

response = client.scan(
    TableName='btc_candles_5m',
)

with open("btc_candles_5m.txt", "w") as outfile:
    json.dump(response, outfile)

print(response)