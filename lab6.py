import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Функція для отримання історичних даних від Coinbase API
def get_historical_data(product_id, granularity, start_time, end_time):
    url = f"https://api.pro.coinbase.com/products/{product_id}/candles"
    params = {
        'start': start_time.isoformat(),
        'end': end_time.isoformat(),
        'granularity': granularity
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('time', inplace=True)
        return df
    else:
        print("Error:", response.status_code)
        return None

# Функція для побудови графіків свічок
def plot_candles(df, ax, product, period):
    ax.plot(df.index, df['low'], color='red', linewidth=1)
    ax.plot(df.index, df['high'], color='green', linewidth=1)
    ax.plot(df.index, df['open'], color='blue', linewidth=1)
    ax.plot(df.index, df['close'], color='black', linewidth=1)
    ax.set_title(f"{product} - {period}")

# Список продуктів для аналізу
products = ['BTC-USD', 'ETH-USD', 'LTC-USD']

# Отримання історичних даних для кожного продукту за останній день, місяць та рік
current_time = datetime.now()
start_day = current_time - timedelta(days=1)
start_month = current_time - timedelta(days=30)
start_year = current_time - timedelta(days=365)

dataframes = {}

for product in products:
    dataframes[product] = {
        'day': get_historical_data(product, 3600, start_day, current_time),  # granularity = 1 година
        'month': get_historical_data(product, 21600, start_month, current_time),  # granularity = 6 годин
        'year': get_historical_data(product, 86400, start_year, current_time)  # granularity = 1 день
    }

# Побудова графіків
fig, axs = plt.subplots(len(products), 3, figsize=(15, 10))
for i, product in enumerate(products):
    for j, period in enumerate(['day', 'month', 'year']):
        plot_candles(dataframes[product][period], axs[i, j], product, period)

plt.tight_layout()
plt.show()


# Базовий статистичний аналіз
for product in products:
    for period, df in dataframes[product].items():
        print(f"Product: {product}, Period: {period}")
        print("Mean:")
        print(df.mean())
        print("Standard Deviation:")
        print(df.std())
        print("Rolling Standard Deviation (10 days):")
        print(df['close'].rolling(window=10).std())
        print("Rolling Standard Deviation (20 days):")
        print(df['close'].rolling(window=20).std())
        print("Rolling Standard Deviation (50 days):")
        print(df['close'].rolling(window=50).std())
        print("\n")
