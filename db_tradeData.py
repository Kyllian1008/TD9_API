import requests
import mysql.connector
from datetime import datetime
from mysql.connector import pooling

db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="trade_data",
    pool_size=5,
    host="localhost",
    user="kyllian2",
    password="cash7823",
    database="blockchainprogapi"
)

def insert_trade_data(cursor, pair, trade):
    trade_id = trade['id']
    price = trade['price']
    quantity = trade['qty']
    timestamp = datetime.utcfromtimestamp(trade['time'] / 1000.0)
    is_buyer_maker = trade['isBuyerMaker']

    query = (
        "INSERT INTO trade_data (trade_id, pair, price, quantity, timestamp, is_buyer_maker) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    cursor.execute(query, (trade_id, pair, price, quantity, timestamp, is_buyer_maker))

def get_trade_data(pair='BTCUSDT', limit=500):
    base_url = "https://api.binance.com/api/v3/trades"

    params = {
        'symbol': pair,
        'limit': limit,
    }

    try:
        connection = db_pool.get_connection()
        cursor = connection.cursor()

        response = requests.get(base_url, params=params)
        response.raise_for_status()  

        data = response.json()

        if not data:
            print(f"No trade data available for {pair}.")
            return

        for trade in data:
            insert_trade_data(cursor, pair, trade)

        connection.commit()
        print("Trade data inserted successfully!")

    except requests.exceptions.RequestException as e:
        print(f"Error making request to Binance API: {e}")

    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


get_trade_data(pair='BTCUSDT', limit=10)
