from my_coin import app
from flask import redirect, render_template, request, jsonify
from my_coin.conection import *
import requests
from my_coin.models import *


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/v1/endpoint1")
def prueba():
    api = ConexionApi()
    datos = json_cleaner(api.get_first_10())
    return jsonify ({
        "datos": datos,
        "status": "ok" 
    })


@app.route("/api/prueba")
def prueba1():
    api = ConexionApi()
    datos = api.get_coin_price(1,1)

    return jsonify({
        "datos": api.get_coin_price(1,1),
        "status": "Ok"
    })
        



   
    
    

     

