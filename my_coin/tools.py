from my_coin.utils import *




def get_coin_id(coinName):
    for name, id in COIN_ID.items():
        if name == coinName:
            return id


def get_all_movements():
    pass    

def get_price_from_json(lista):
    price = lista["data"]["quote"]["EUR"]["price"]
    return price
 

def get_coin_ids(incoming_dic, new_dic):
    for i in incoming_dic["data"]:
        new_dic[i["name"].lower()]= i["id"] 