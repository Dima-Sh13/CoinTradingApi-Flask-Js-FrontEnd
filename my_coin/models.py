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
        
def buy_coin_exchange(coin_from, coin_to, amount_from):
    api = ConexionApi()
    units_to_buy = 0
    if coin_from == "EUR":
        coin_from_price = amount_from
        coin_to_price= api.get_coin_price(coin_to)
        units_to_buy= coin_from_price/coin_to_price
    elif coin_to == "EUR":
        coin_from_price = api.get_coin_price(coin_from, amount=amount_from)
        units_to_buy= coin_from_price * amount_from
    else:
        coin_from_price = api.get_coin_price(coin_from, amount=amount_from)
        coin_to_price= api.get_coin_price(coin_to)
        units_to_buy= coin_from_price/coin_to_price    
    
    return units_to_buy

def get_coin_id():
    pass