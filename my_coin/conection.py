import sqlite3
from requests import Session
import json
from config import API_KEY,DATA_BASE
from my_coin.utils import *
from my_coin.tools import *
from decimal import Decimal
class ConexionApi(Session):
    def __init__(self,timeout: float = 10.0):
        super().__init__()
        self.BASE_URL = "https://pro-api.coinmarketcap.com"
        self.timeout = timeout
        self.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY,
            })
       

    def get_first_100(self):
        self.params = { 
            "limit":"100",
            "convert": "EUR"}
        response = self.get(f"{self.BASE_URL}/v1/cryptocurrency/listings/latest", timeout=self.timeout)
        data = response.json()
        return data

    def get_coin_price(self,coin_name, amount = 1):
        """
        Funcion para conseguir el precio unitario de cada moneda, se debe pasar el id
        de la moneda en int.
        Devuelve el precio unitario formateado.
        """
        
        coin_id = get_coin_id(coin_name)
        
        self.params = {
            "id":coin_id,
            "amount":amount,
            "convert": "EUR",
            
        }
        response = self.get(f"{self.BASE_URL}/v2/tools/price-conversion", timeout=self.timeout)
        data = response.json()
        unit_price = get_price_from_json(data)  
        return float(unit_price)
        
    
        

class ConexionBD():
    def __init__(self):
        self.db_path = DATA_BASE

    def buy_coin(self, params=[]):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO movements (datetime, coin_from, amount_from, coin_to, amount_to, price_per_unit) VALUES (?,?,?,?,?,?)",
                params
            )

  

    def get_all_movements(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT datetime, coin_from, amount_from, coin_to, amount_to, price_per_unit FROM movements;")
            rows = cur.fetchall()
        return rows

    def get_coin_amount(self, coin):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT
                  ? AS coin,
                  COALESCE(SUM(CASE WHEN LOWER(coin_to)   = LOWER(?) THEN amount_to   ELSE 0 END), 0)
                - COALESCE(SUM(CASE WHEN LOWER(coin_from) = LOWER(?) THEN amount_from ELSE 0 END), 0)
                  AS amount
                FROM movements;
                """,
                (coin, coin, coin)
            )
            row = cur.fetchall()  
        return row[0][1]

    def update_wallet(self, coin):
        amount = self.get_coin_amount(coin)
        with sqlite3.connect(self.db_path, timeout=10) as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO wallet (coin, amount)
                VALUES (?, ?)
                ON CONFLICT(coin) DO UPDATE SET amount = excluded.amount;
                """,
                (coin, amount)
            )

    def get_wallet(self):
        with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT coin, amount FROM wallet;
                """
            )
            rows = cur.fetchall()
            return rows

    def get_wallet_by_coin(self,coin):
         with sqlite3.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute(f"SELECT coin, amount FROM wallet WEHERE {coin} = coin;"
            )
               
            rows = cur.fetchall()
            return rows

class Status():
    def __init__(self):
        self.api = ConexionApi()
        self.dataBase = ConexionBD()


    def invested(self):
        with sqlite3.connect(self.dataBase.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT SUM(amount_from) FROM movements where coin_from = 'EUR' ;")
            
            invested = cur.fetchone()
            if invested[0] == None:
                invested = 0
            else:
                invested = invested[0]
        return Decimal(invested)
        
    def recovered(self):
        with sqlite3.connect(self.dataBase.db_path) as con:
            cur = con.cursor()
            cur.execute("SELECT SUM(amount_to) FROM movements where coin_to = 'EUR' ;")
            
            recovered = cur.fetchone()
            if recovered[0] == None:
                recovered = 0
            else:
                recovered = recovered[0]
        return Decimal(recovered)
    
    def valor_compra(self):
        invertido = self.invested()
        recuperado = self.recovered()
        value = invertido- recuperado
        return value
    
    def current_wallet_value(self):
        total_wallet_value = Decimal()
        wallet_list= self.dataBase.get_wallet()
        for i in wallet_list:
            total_wallet_value += Decimal(self.api.get_coin_price(i[0],i[1]))

        return total_wallet_value


        
        