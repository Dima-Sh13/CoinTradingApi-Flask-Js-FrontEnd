from . import app
from flask import redirect, render_template, request, jsonify
from my_coin.conection import *
import requests
from my_coin.models import *
from datetime import datetime
ahora = datetime.now()
t_now = ahora.strftime("%Y-%m-%d %H:%M:%S")

from my_coin import app
from my_coin.tools import *
from my_coin.utils import *




@app.route("/")
def index():
    bd=ConexionBD()
    
    return render_template("index.html", coins = get_aviable_coins())
    
   
    

@app.route("/api/v1/endpoint1")
def prueba():
    api = ConexionApi()
    
    datos =api.get_first_10()
    get_coin_ids_test(datos, prueba_coin_id)
    return jsonify ({
        "datos": prueba_coin_id,
        "status": "ok" 
    })


@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>", methods=["POST"])
def exchange_rate(moneda_from, moneda_to):
    # intentamos parsear JSON de forma segura
    data = request.get_json(force=True, silent=True)
    if not data or "amount" not in data:
        return jsonify({"status":"fail", "mensaje":"No se recibió 'amount' en JSON"}), 400
    try:
        amount_from = float(data["amount"])
    except (TypeError, ValueError):
        return jsonify({"status":"fail", "mensaje":"'amount' no es numérico"}), 400

    amount_aviable_to_purchase = buy_coin_exchange(moneda_from, moneda_to, amount_from)
    # devolvemos ambas formas (underscore y camelCase) para evitar problemas de clave
    return jsonify({
        "purchased_amount": amount_aviable_to_purchase,
        "purchasedAmount": amount_aviable_to_purchase,
        "status": "OK"
    })


        
"""
@app.route("/api/v1/tasa/<moneda_from>/<moneda_to>/<amount_from>", methods=["POST"])
def exchange_rate(moneda_from,moneda_to,amount_from):
    
    
    
    amount_aviable_to_purchase = buy_coin_exchange(moneda_from,moneda_to, amount_from)
    return jsonify({
        "purchasedAmount":amount_aviable_to_purchase,
        "status":"OK"

    })    
    
    return jsonify({
        "datos":amount_from
    })
    
"""
    


@app.route("/api/v1/movimientos", methods =["GET"])
def all_movements():
    bd=ConexionBD()
    all_movements = bd.get_all_movements()
    return jsonify({
        "datos": all_movements,
        "status": "Ok"
    })
    

    

@app.route("/api/v1/compra", methods=["POST"])
def buy_coin():
    bd=ConexionBD()
    api = ConexionApi()
    datos = request.json
    pu = api.get_coin_price(datos["moneda_to"])
    bd.buy_coin([t_now,datos["moneda_from"],datos["amount_from"],datos["moneda_to"],buy_coin_exchange(datos["moneda_from"],datos["moneda_to"],datos["amount_from"]),pu])
    
    return jsonify({
        "message":"Purchase Done!",
        "status":"ok"

    })


    

@app.route("/api/v1/status")
def show_status():
   pass
   
    
    

     

