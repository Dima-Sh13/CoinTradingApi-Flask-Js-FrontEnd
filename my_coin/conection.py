import sqlite3
from requests import Request, Session

import json
url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
def conexion():
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': "e197777064bf438bbf96a6c2145bb120",
    }


    session = Session()
    session.headers.update(headers)

    response = session.get(url)
    data = json.loads(response.text)
    return data