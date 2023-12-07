import requests
#   -------------------   Here are the GET Functions ---------------------

# First GET function
def get_all_binance_cryptocurrencies():
    base_url = "https://api.binance.com/api/v3/exchangeInfo"

    try:
        response = requests.get(base_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        symbols = [symbol_info['symbol'] for symbol_info in data['symbols']]
        return symbols
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Binance API: {e}")
        return None

# Second GET function 
def get_depth(direction='ask', pair='BTCUSDT'):
    base_url = "https://api.binance.com/api/v3/depth"
    params = {"symbol": pair}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        if direction == 'ask':
            price = float(data['asks'][0][0])
        elif direction == 'bid':
            price = float(data['bids'][0][0])
        else:
            print("Invalid direction. Use 'ask' or 'bid'.")
            return None

        return price
    except requests.exceptions.RequestException as e:
        print(f"Error making request to Binance API: {e}")
        return None
    
#Third GET function 
import requests

def get_order_book(pair='BTCUSDT', limit=5):
    base_url = "https://api.binance.com/api/v3/depth"
    params = {"symbol": pair, "limit": limit}

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()
        
        # Extract bids and asks from the response
        bids = data.get('bids', [])
        asks = data.get('asks', [])

        # Format and print the order book
        print(f"Order Book for {pair}:")
        print("Bids:")
        for bid in bids:
            print(f"Price: {bid[0]}, Quantity: {bid[1]}")
        
        print("\nAsks:")
        for ask in asks:
            print(f"Price: {ask[0]}, Quantity: {ask[1]}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Binance API: {e}")


#Fourth GET function
import requests

def refreshDataCandle(pair='BTCUSDT', duration='5m', latest_timestamp=16415520):
    base_url = "https://api.binance.com/api/v3/klines"
    
    params = {
        'symbol': pair,
        'interval': duration,
    }

    if latest_timestamp:
        params['startTime'] = latest_timestamp + 1  # Fetch data starting from the next timestamp

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        if not data:
            print("No new candlestick data available.")
            return

        # Update the latest timestamp
        latest_timestamp = int(data[-1][0])

        # Format and print the candlestick data
        print(f"\nCandlestick Data for {pair} ({duration} intervals):")
        print("Open time\t\tOpen\t\tHigh\t\tLow\t\tClose\t\tVolume")

        for candle in data:
            print(f"{candle[0]}\t{candle[1]}\t{candle[2]}\t{candle[3]}\t{candle[4]}\t{candle[5]}")

        print(f"Latest timestamp: {latest_timestamp}")

        # You can save the latest timestamp to a file or database for future use

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Binance API: {e}")

#Fifth GET function
def getTradeData(pair, limit=500):
    base_url = "https://api.binance.com/api/v3/trades"

    params = {
        'symbol': pair,
        'limit': limit,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        if not data:
            print(f"No trade data available for {pair}.")
            return

        # Format and print the trade data
        print(f"\nTrade Data for {pair}:")
        print("Trade ID\tPrice\t\tQty\t\tTime\t\t\t\tIs Buyer Maker")

        for trade in data:
            print(f"{trade['id']}\t\t{trade['price']}\t{trade['qty']}\t{trade['time']}\t{trade['isBuyerMaker']}")

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Binance API: {e}")


def main():
    print("Choose a function to run:")
    print("1. Get all Binance cryptocurrencies")
    print("2. Get Binance depth price")
    print("3. Get order book for an asset")
    print("4. Read agregate trading data")
    print("5. Extract all trade data")

    choice = input("Enter the number of the function: ")

    if choice == '1':
        all_symbols = get_all_binance_cryptocurrencies()
        if all_symbols:
            print("List of all available cryptocurrencies on Binance:")
            print('\n'.join(all_symbols))
        else:
            print("Error retrieving the list of cryptocurrencies.")

    elif choice == '2':
        direction = input("Enter 'ask' or 'bid' for depth: ")
        pair_name = input("Enter the trading pair symbol: ")
        depth_price = get_depth(direction, pair_name)
        if depth_price is not None:
            print(f"{direction} price for {pair_name}: {depth_price}")
        else:
            print("Error retrieving depth price.")

    elif choice == '3':
        pair_name = input("Enter a pair name : ")
        get_order_book(pair_name)

    elif choice == '4':
        pair_name = input("Enter a pair name : ")
        refreshDataCandle(pair_name)
    
    elif choice == '5':
        pair = input("Enter a pair name : ")
        getTradeData(pair)

    else:
        print("Invalid choice. Please enter '1' or '2' or '3' or '4'.")

if __name__ == "__main__":
    main()
