import requests
import hashlib
import hmac
import time

def create_order(api_key, secret_key, direction, price, amount, pair='BTCUSD_d', order_type='LimitOrder'):
    base_url = "https://api.example.com/create_order"  # Replace with the actual API endpoint

    # Create a nonce (timestamp)
    nonce = str(int(time.time() * 1000))

    # Create the request payload
    payload = {
        "api_key": api_key,
        "nonce": nonce,
        "direction": direction,
        "price": price,
        "amount": amount,
        "pair": pair,
        "order_type": order_type,
    }

    # Create the signature
    signature = hmac.new(secret_key.encode(), msg=str(payload).encode(), digestmod=hashlib.sha256).hexdigest()

    # Include the signature in the request headers
    headers = {
        "Content-Type": "application/json",
        "Signature": signature,
    }

    try:
        # Send the POST request
        response = requests.post(base_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        data = response.json()

        if data.get('status') == 'success':
            print("Order created successfully.")
            print("Order ID:", data.get('order_id'))
        else:
            print("Failed to create order. Error:", data.get('error'))

    except requests.exceptions.RequestException as e:
        print(f"Error making request to the API: {e}")

# Example usage
api_key = "your_api_key"
secret_key = "your_secret_key"
direction = "buy"  # or "sell"
price = 100.0  # Replace with your desired price
amount = 1.0  # Replace with your desired amount

create_order(api_key, secret_key, direction, price, amount)
