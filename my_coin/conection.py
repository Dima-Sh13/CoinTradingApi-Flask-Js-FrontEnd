import sqlite3
from requests import Request, Session

import json
url = 'https://pro-api.coinmarketcap.com//v1/cryptocurrency/listings/latest'
def conexion():
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': "e197777064bf438bbf96a6c2145bb120",
    }

    parameters = {
  
  
  "convert":"EUR"
}
    session = Session()
    session.headers.update(headers)

    response = session.get(url)
    data = json.loads(response.text)
    return data

class ConexionApi(Session):
    def __init__(self):
        super().__init__()
        self.BASE_URL = "https://pro-api.coinmarketcap.com/"
        self.headers.update({
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': "e197777064bf438bbf96a6c2145bb120",
            })
        self.params = { 
            "limit":"10",
            "convert": "EUR"}

    def get_first_10(self):
        response = self.get(f"{self.BASE_URL}/v1/cryptocurrency/listings/latest")
        data = response.json()
        return data