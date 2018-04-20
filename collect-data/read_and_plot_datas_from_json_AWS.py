import json
from pprint import pprint
import matplotlib.pyplot as plt
import datetime

debug=False

data = json.load(open('btc_candles_5m.txt'))

candle_low=[]
candle_close=[]
candle_volume=[]
candle_high=[]
candle_mts=[]
candle_mts_int=[]
candle_open=[]

candles=[]

plot_date_counter=0
for trade in data["Items"]:
	plot_date_counter=plot_date_counter+1

	if (debug):
		print("low : ", trade["low"]["S"])
	candle_low.append(trade["low"]["S"])
	if (debug):
		print("close : ", trade["close"]["S"])				
	candle_close.append(trade["close"]["S"])
	if (debug):
		print("volume : ", trade["volume"]["S"])
	candle_volume.append(trade["volume"]["S"])
	if (debug):
		print("high : ", trade["high"]["S"])
	candle_high.append(trade["high"]["S"])
	if (debug):
		print("mts : ", trade["mts"]["S"])
	candle_mts.append(trade["mts"]["S"])
	if (debug):
		print("mts_int : ", int(trade["mts"]["S"]))
	candle_mts_int.append(int(trade["mts"]["S"]))
	if (debug):
		print("open : ", trade["open"]["S"], '\n')
	candle_open.append(trade["open"]["S"])

	candles.append((int(trade["mts"]["S"]), float(trade["open"]["S"]), float(trade["close"]["S"]), float(trade["high"]["S"]), float(trade["low"]["S"]), float(trade["volume"]["S"])))

print("number of trades : ",plot_date_counter)

# Sort lists according to mts
#Z = [x for _, x in sorted(zip(candle_mts_int,candle_low), key=lambda pair: pair[0])]

#print(candles)
sorted_by_mts = sorted(candles, key=lambda tup: tup[0])
#print("sorted by mts :", sorted_by_mts)

for candle in sorted_by_mts:
	print(candle)

#print("candles mts sorted : ",sorted(candle_mts_int))
#print("candles max mts :",max(candle_mts_int));
# Plot datas
#plt.scatter(ids,price,s=1)
#plt.xlabel('timestamp')
#plt.ylabel('price')
#plt.show()