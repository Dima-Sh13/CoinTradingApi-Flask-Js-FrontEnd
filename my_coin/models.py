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
        
def buy_coin(eur, coin_name):
    api = ConexionApi()
    coin_price= api.get_coin_price(coin_name)
    units_to_buy= eur/float(coin_price)
    return units_to_buy

def get_coin_id():
    pass