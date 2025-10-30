from my_coin.utils import *




def get_coin_id(coinName):
    for name, id in COIN_ID.items():
        if name == coinName.lower():
            return id
"""
def get_coin_id(coinName):
    for name, id in prueba_coin_id.items():
        if name == coinName.lower():
            return id

"""            
def get_aviable_coins(incoming_dict):
    """
    new_dict = {}
    for i in incoming_dict["data"]:
        new_dict[i["name"].lower()]= i["id"] 

    """
    aviable_coins = []
    for name, id in incoming_dict.items():
        aviable_coins.append(name.capitalize())

    return aviable_coins    

def get_all_movements():
    pass    

def get_price_from_json(lista):
    price = lista["data"]["quote"]["EUR"]["price"]
    return price
 

def get_coin_ids_test(incoming_dic, new_dict):
    
    for i in incoming_dic["data"]:
        new_dict[i["name"].lower()]= i["id"] 

        