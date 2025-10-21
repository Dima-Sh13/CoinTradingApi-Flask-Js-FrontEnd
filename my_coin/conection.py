import sqlite3
from requests import Session
import json
from config import API_KEY,DATA_BASE

class ConexionApi(Session):
    def __init__(self):
        super().__init__()
        self.BASE_URL = "https://pro-api.coinmarketcap.com/"
        self.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': API_KEY,
            })
        self.params = { 
            "limit":"10",
            "convert": "EUR"}

    def get_first_10(self):
        response = self.get(f"{self.BASE_URL}/v1/cryptocurrency/listings/latest")
        data = response.json()
        return data
    

class ConexionBD():
      def __init__(self,querySql,params=[]):
        self.con = sqlite3.connect(DATA_BASE)
        self.cur = self.con.cursor()
        self.res = self.cur.execute(querySql, params)
