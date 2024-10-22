import sqlite3
from flask import Flask, render_template, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
import db
from db import DaBa
import asyncio
from adminPanelMethods import adminControl
from servers import reverseServer1, reverseServer2, reverseServer3
from flask_login import LoginManager, login_user, login_required, current_user, logout_user



app = Flask(__name__, static_folder="www/files", template_folder="www")
app.config["SECRET_KEY"] = "iojoijoijoijjijjkjlbhyuglftdfyugf7y"
login_manager=LoginManager(app)


@app.route("/")
@app.route("/Registration_user.html")
@app.route("/Registration_user.html", methods=["POST"])
async def index():
    await db.initialize_pool()
    if request.method == "POST":
        if request.form["email"] == "123" and request.form["password"] == "123":
            Admins = await reverseServer1.getAllAdmins()
            # print(Admins)
            return redirect("Main_menu.html")
    return render_template("Registration_user.html")


@app.route("/Main_menu.html")
# @app.route("/Main_menu.html", methods=["POST"])
def menu():
    return render_template("Main_menu.html")


@app.route("/Filtering_rules.html")
@app.route("/Filtering_rules.html", methods=["POST"])
async def filter():
    if request.method == "POST":
        if request.form["type"] == "mask":
            await adminControl().changeMaskMethod(1)
        if request.form["type"] == "delete":
            await adminControl().changeMaskMethod(2)
        if request.form["type"] == "filter":
            await adminControl().changeMaskMethod(3)
        return redirect("Filtering_rules.html")
    return render_template("Filtering_rules.html")


@app.route("/data_sorce.html")
def source():
    return render_template("data_sorce.html")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app.run(host='0.0.0.0', port=5052, debug=True)
