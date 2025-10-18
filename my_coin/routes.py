from my_coin import app
from flask import redirect, render_template, request
import http



@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html")