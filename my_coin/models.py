import sqlite3
import requests
from config import API_KEY

from my_coin.conection import *
from datetime import datetime
from my_coin.conection import *
t_now = datetime.now()



def json_cleaner(json):
    json_clean = []
    for i in json["data"]:
        
        json_clean.append({
            "name": i["name"],
            "symbol": i["symbol"],
            "pu_EUR":i["quote"]["EUR"]["price"],
            "timestamp": json["status"]["timestamp"]
        })
    
    return json_clean
        
def buy_coin_exchange(coin_from, coin_to):
    api = ConexionApi()
    coin_from_price = api.get_coin_price(coin_from)
    #coin_from_price = get_price_from_json(coin_from)
    coin_to_price= api.get_coin_price(coin_to)
    #coin_to_price = get_price_from_json(coin_to_data)
   
    units_to_buy= coin_from_price/coin_to_price
    return units_to_buy

def get_coin_id():
    pass