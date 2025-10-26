import sqlite3
from requests import Session
import json
from config import API_KEY,DATA_BASE
from my_coin.utils import *
from my_coin.tools import get_coin_id

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

    def get_coin_price(self,coin_name):
        """
        Funcion para conseguir el precio unitario de cada moneda, se debe pasar el id
        de la moneda en int.
        Devuelve el precio unitario formateado.
        """
        coin_id = get_coin_id(coin_name.capitalize())
        self.params = {
            "id":coin_id,
            "amount":1,
             "convert": "EUR"  
        }
        response = self.get(f"{self.BASE_URL}/v2/tools/price-conversion")
        data = response.json()
        unit_price = data["data"]["quote"]["EUR"]["price"]   
        return f"{unit_price:.2f}"

    
        

class ConexionBD():
    def __init__(self):
        self.con = sqlite3.connect(DATA_BASE)
        self.cur = self.con.cursor()
        
    

    def buy_coin(self,params=[]):
        self.res = self.cur.execute(f"INSERT INTO movements (datetime, coin_from, amount_from, coin_to, amount_to, price_EUR) VALUES (?,?,?,?,?,?) ",params)
        self.con.commit()
        self.con.close()
    def trade_coin(self,coin_from, coin_to):
        pass

    def sell_coin(self,coin_from):
        pass 

    def get_all_movements(self):
        self.res = self.cur.execute("SELECT datetime, coin_from, amount_from, coin_to, amount_to, price_EUR FROM movements;")
        rows = self.cur.fetchall()
        self.con.close()
        return rows
    
    def get_coin_amount(self,coin):
        
        self.res = self.cur.execute(
            """SELECT
            COALESCE(SUM(CASE WHEN coin_to   = ? THEN amount_to   ELSE 0 END), 0)
            - COALESCE(SUM(CASE WHEN coin_from = ? THEN amount_from ELSE 0 END), 0)
            AS saldo
            FROM movements;""",(coin,coin))
        
        wallet = self.cur.fetchone()[0]
        self.con.close()

        return wallet
    
    def update_wallet(self, coin):
        amount = self.get_coin_amount()
        self.res = self.cur.execute("""
            INSERT INTO wallet (coin, amount)
            VALUES (?, ?)
            ON CONFLICT(coin) DO UPDATE SET amount = excluded.amount;
        """, (coin, amount))
        self.con.commit()
        self.con.close()
        
