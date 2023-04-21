import requests

base_url = 'http://188.138.122.94:8090'
instrument = 'BTCUSDT'
server_time_endpoint = '/paper/api/bnf/servertime'
get_last_tick_endpoint = "/paper/api/bnf/backtest/last-tick"
place_order_endpoint = "/paper/api/bnf/orders/place"
start_backtest_endpoint = f"/paper/api/bnf/backtest/{instrument}/start"
stop_backtest_endpoint = f"/paper/api/bnf/backtest/stop"


def get_request(endpoint, params=None, headers=None):
    url = base_url + endpoint
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print('Failed to make request. Status code:', response.status_code)
        return None

# Get server time
server_time_headers = {
   'X_BOT':'X-BOT',
    'sign':'sign'
}

get_last_tick_headers = {
   'X-BOT':'X-BOT',
    'sign':'sign'
}

def start_backtest(instrument):
    start_backtest_endpoint = f"/paper/api/bnf/backtest/{instrument}/start"
    headers = {
        "X-BOT": "X-BOT",
        "sign": "sign"
    }

    params = {
    'loopspeed': "10",
     'backtestnumber':"1",
     'startequity':"1000"
    }
    
    response = requests.post(
        base_url + start_backtest_endpoint,
        headers=headers,params=params
    )
    
    if response.status_code == 200:
        print("Backtest started successfully")
        return True
    else:
        print("Failed to start backtest. Status code:", response)
        return False
    
    
def stop_backtest():
    stop_backtest_endpoint = f"/paper/api/bnf/backtest/stop"
    
    headers = {
        "X-BOT": "X-BOT",
        "sign": "sign"
    }
    response = requests.post(
        base_url + stop_backtest_endpoint,
        headers=headers
    )
    
    if response.status_code == 200:
        print("Backtest stopped successfully")
        return True
    else:
        print("Failed to stop backtest. Status code:", response)
        return False
    
    
def place_order(side,quantity):
    
    headers = {
        "X-BOT": "X-BOT",
        "sign": "sign"
    }

    data = {
        'symbol': 'BTCUSDT',
        'side': side,
        'quantity': quantity,
        'timestamp': f"{get_request(server_time_endpoint)['timestamp']}",
        'price': f"{get_request(get_last_tick_endpoint,headers=get_last_tick_headers)['ask']*1.01}"
    }

    response = requests.post(
            base_url + place_order_endpoint,
            headers=headers,
            json=data)
    print(response.json())