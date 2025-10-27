
COIN_ID = {
    "bitcoin": 1,
    "ethereum": 1027,
    "tether usdt": 825,
    "bnb": 1839,
    "xrp": 52,
    "solana": 5426,
    "usdc": 3408,
    "tron": 1958,
    "dogecoin": 74,
    "cardano": 2010,
    "polkadot": 6636,
    "polygon": 3890
}



def get_coin_id(coinName):
    for name, id in COIN_ID.items():
        if name == coinName:
            return id


def get_all_movements():
    pass    

def get_price_from_json(lista):
    price = lista["data"]["quote"]["EUR"]["price"]
    return price
