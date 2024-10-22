import sqlite3
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import db
from db import DaBa
from servers import reverseServer1, reverseServer2, reverseServer3
app = Flask(__name__, static_folder="www/files", template_folder="www")
app.config["SECRET_KEY"]="iojoijoijoijjijjkjlbhyuglftdfyugf7y"
import asyncio

@app.route("/")
@app.route("/Registration_user.html")
@app.route("/Registration_user.html", methods=["POST"])
async def index():
    if request.method=="POST":
        if request.form["email"]=="123" and request.form["password"]=="123":
            Admins = await reverseServer1.getAllAdmins()
            print(Admins)
            return redirect("Main_menu.html")
    return render_template("Registration_user.html")

@app.route("/Main_menu.html")
#@app.route("/Main_menu.html", methods=["POST"])
def menu():
    return render_template("Main_menu.html")

@app.route("/Filtering_rules.html")
def filter():
    return render_template("Filtering_rules.html")

@app.route("/data_sorce.html")
def source():
    return render_template("data_sorce.html")

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port="5052", debug=True)
