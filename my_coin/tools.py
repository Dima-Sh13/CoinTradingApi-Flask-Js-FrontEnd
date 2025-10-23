from my_coin.utils import *

def get_coin_id(coinName):
    for name, id in COIN_ID.items:
        if name == coinName:
            return id