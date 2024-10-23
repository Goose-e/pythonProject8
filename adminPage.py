from asyncio import WindowsSelectorEventLoopPolicy
from UserLogin import fromBD
from flask import Flask, render_template, request, redirect
import db
from db import DaBa
from UserLogin import UserLogin
import asyncio
from adminPanelMethods import adminControl
from servers import reverseServer1
from flask_login import LoginManager, login_user, login_required, logout_user

app = Flask(__name__, static_folder="www/files", template_folder="www")
app.config["SECRET_KEY"] = "iojoijoijoijjijjkjlbhyuglftdfyugf7y"
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return asyncio.get_running_loop().run_until_complete(fromBD(user_id, DaBa()))

@app.route("/", methods=["GET", "POST"])
@app.route("/Registration_user.html", methods=["GET", "POST"])
async def index():
    await db.initialize_pool()
    if request.method == "POST":
        check = await reverseServer1.authAdmin(request.form["email"], request.form["password"])
        print(check)
        if check and check.get_id() is not None:
            LM = UserLogin()
            await LM.createUser(check)
            login_user(LM.get_user())
            return redirect("Main_menu.html")
        else:
            return render_template("Registration_user.html")
    return render_template("Registration_user.html")


@app.route("/Main_menu.html")
@login_required
def menu():
    return render_template("Main_menu.html")


@app.route("/Filtering_rules.html", methods=["GET", "POST"])
@login_required
async def filter():
    if request.method == "POST":
        action_type = request.form["type"]
        if action_type == "mask":
            await adminControl().changeMaskMethod(1)
        elif action_type == "delete":
            await adminControl().changeMaskMethod(2)
        elif action_type == "filter":
            await adminControl().changeMaskMethod(3)
        return redirect("Filtering_rules.html")
    return render_template("Filtering_rules.html")


@app.route("/data_source.html")
@login_required
def source():
    return render_template("data_source.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("Registration_user.html")


if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    app.run(host='0.0.0.0', port=5052, debug=True)
