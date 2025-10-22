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
    
    datos = buy_coin(95000,1)

    return jsonify({
        "datos": datos,
        "status": "Ok"
    })
        

@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>")
def exchange_rate(moneda_from,moneda_to):
    
    pass


@app.route("/api/v1/movimientos")
def all_movements():
    

    pass

@app.route("/api/v1/compra", methods=["POST"])
def buy_coin():
    datos = request.json
    return print(datos)

    

@app.route("/api/v1/status")
def show_status():
    pass

   
    
    

     

