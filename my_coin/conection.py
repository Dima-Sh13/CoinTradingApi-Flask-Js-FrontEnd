import sqlite3
from requests import Session
import json
from config import API_KEY,DATA_BASE

class ConexionApi(Session):
    def __init__(self):
        super().__init__()
        self.BASE_URL = "https://pro-api.coinmarketcap.com"
        self.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY,
            })
       

    def get_first_10(self):
        self.params = { 
            "limit":"10",
            "convert": "EUR"}
        response = self.get(f"{self.BASE_URL}/v1/cryptocurrency/listings/latest")
        data = response.json()

        return data
    def get_coin_price(self,id):
        """
        Funcion para conseguir el precio unitario de cada moneda, se debe pasar el id
        de la moneda en int.
        Devuelve el precio unitario formateado.
        """
        self.params = {
            "id":id,
            "amount":1,
             "convert": "EUR"  
        }
        response = self.get(f"{self.BASE_URL}/v2/tools/price-conversion")
        data = response.json()
        unit_price = data["data"]["quote"]["EUR"]["price"]   
        return f"{unit_price:.2f}"

    
        

class ConexionBD():
    def __init__(self,querySql):
        self.con = sqlite3.connect(DATA_BASE)
        self.cur = self.con.cursor()
        
    def get_coin_amount(self, querySql):
        self.res = self.cur.execute(querySql)

    def buy_coin(self,coin_to):
        self.res = self.cur.execute(f"INSERT INTO movements (date, time, coin_from, amount_from, coin_to, amount_to, price_EUR) VALUES () ")

    def trade_coin(self,coin_from, coin_to):
        pass

    def sell_coin(self,coin_from):
        pass  