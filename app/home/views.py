from flask import render_template

from . import home

@home.route("/")
def index():
    return render_template("home/index.html")

@home.route("/charts")
def charts():
   return render_template("home/charts.html")