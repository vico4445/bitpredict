from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal

client = boto3.client('dynamodb')

response = client.get_item(
    TableName='btc_trades',
    Key={ 
        '_id': {
            'S': '1515278891341',
        },
    },
)

with open('btc_item.txt', 'w') as outfile:
    json.dump(response, outfile)

print(response)
