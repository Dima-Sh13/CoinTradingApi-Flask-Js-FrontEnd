from my_coin import app
from flask import redirect, render_template, requests, jsonify



@app.route("/")
def index():
    return render_template("index.html")