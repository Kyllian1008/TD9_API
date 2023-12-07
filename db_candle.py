import requests
import mysql.connector
from datetime import datetime

def fetch_candlestick_data(pair, interval):
    base_url = f"https://api.binance.com/api/v3/klines?symbol={pair}&interval={interval}"

    response = requests.get(base_url)
    response.raise_for_status()
    candlestick_data = response.json()
    return candlestick_data

def insert_candlestick_data(cursor, pair, interval):
    candlestick_data = fetch_candlestick_data(pair, interval)

    for candlestick in candlestick_data:
        timestamp = datetime.utcfromtimestamp(candlestick[0] / 1000.0)
        timestamp_unix = int(timestamp.timestamp())  # Convert to Unix timestamp
        
        open_price, high, low, close, volume = map(float, candlestick[1:6])
        
        query = (
            "INSERT INTO my_table (date, high, low, open, close, volume) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        cursor.execute(query, (timestamp_unix, high, low, open_price, close, volume))

def main():
    # Replace these values with your actual MySQL connection details
    db_config = {
        "host": "localhost",
        "user": "kyllian2",
        "password": "cash7823",
        "database": "blockchainprogapi",
    }

    pair = "BTCUSDT"
    interval = "5m"

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        insert_candlestick_data(cursor, pair, interval)

        connection.commit()
        print("Candlestick data inserted successfully!")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    main()
