import sqlite3
import requests
from config import API_KEY
from my_coin.conection import *
from datetime import datetime
from my_coin.conection import *
from decimal import Decimal, getcontext 
t_now = datetime.now()

getcontext().prec = 30

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
"""        
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
"""

def buy_coin_exchange(coin_from, coin_to, amount_from):
    
    api = ConexionApi()
    bd = ConexionBD()
    units_to_buy = 0.0
    amount_from_dec = Decimal(amount_from)

    if coin_from == "EUR":
        coin_from_price = amount_from_dec    
        coin_to_price = Decimal(api.get_coin_price(coin_to))
        units_to_buy = coin_from_price / coin_to_price
    elif coin_to == "EUR" and wallet_check(amount_from_dec, bd.get_coin_amount(coin_from)):
        coin_from_price = Decimal(api.get_coin_price(coin_from, amount=amount_from_dec))
        units_to_buy = coin_from_price * amount_from_dec
    else:
        if wallet_check(amount_from_dec, bd.get_coin_amount(coin_from)) == True:
            coin_from_price = Decimal(api.get_coin_price(coin_from, amount=amount_from))
            coin_to_price = Decimal(api.get_coin_price(coin_to))
            units_to_buy = coin_from_price / coin_to_price
        else:
            units_to_buy = f"Cantidad a vender ({amount_from} {coin_from}), mayor que la disponible ({bd.get_coin_amount(coin_from)} {coin_from}))"
    return units_to_buy


def wallet_check(incoming_amount, wallet_amount):
    if incoming_amount > wallet_amount:
        return False
    else:
        return True


