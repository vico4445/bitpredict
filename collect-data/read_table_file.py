import json
from pprint import pprint
import matplotlib.pyplot as plt
import datetime

data = json.load(open('btc_trades.txt'))

ids=[]
price=[]

plot_date_counter=0
for trade in data["Items"]:
	plot_date_counter=plot_date_counter+1
	ids.append(trade["_id"]["S"])
#	ids.append(datetime.datetime.fromtimestamp(float(trade["_id"]["S"])/1000.0).strftime('%Y-%m-%d %H:%M:%S'))
	price.append(trade["price"]["S"])
	#print(datetime.datetime.fromtimestamp(float(trade["_id"]["S"])/1000.0).strftime('%Y-%m-%d %H:%M:%S'))
	#print(trade["price"]["S"])
print("number of trades : %d",plot_date_counter)
# Plot datas
plt.scatter(ids,price,s=1)
plt.xlabel('timestamp')
plt.ylabel('price')
plt.show()