import pandas as pd
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from datetime import timedelta

# read data
all_stats = pd.read_csv('stats/goldx.csv', delimiter=',', nrows=None)
nRow, nCol = all_stats.shape
print(f'There are {nRow} rows and {nCol} columns')

all_stats['Date'] = pd.to_datetime(all_stats.Date)
all_stats = all_stats.sort_values(by='Date')

# get sample
sample_size = 100
stats = all_stats.sample(sample_size)
stats = stats.sort_values(by='Date')

# find delta in days between measurements
d1 = (stats['Date'].iloc[1] - stats['Date'].iloc[0]).days
d2 = (stats['Date'].iloc[2] - stats['Date'].iloc[1]).days
gcd = math.gcd(d1, d2)
for i in range(3, sample_size):
    d = (stats['Date'].iloc[i] - stats['Date'].iloc[i-1]).days
    gcd = math.gcd(gcd, d)
m_delta = gcd

# interpolate sample
dates = list(stats['Date'])
prices = list(stats['Price'])
timestamps = list(map(lambda date: date.timestamp(), dates))
cs = interp1d(timestamps, prices, kind='quadratic')
interpolated_prices = []
interpolated_dates = []
date = dates[0]
while date != dates[-1] + timedelta(days=m_delta):
    interpolated_dates.append(date)
    interpolated_prices.append(cs(date.timestamp()))
    date += timedelta(days=m_delta)

# plot
plt.title('XAU/USD Rate')
plt.xlabel('Time')
plt.ylabel('Rate')
plt.xlim(dates[0], dates[-1])
plt.ylim(0, 2000)
plt.plot(list(all_stats['Date']), list(all_stats['Price']), label='real rate')
plt.plot(interpolated_dates, interpolated_prices, label='interpolated rate')
plt.plot(dates, prices, "r.", markersize=5)
plt.legend(loc='lower right', ncol=2)
plt.show()
