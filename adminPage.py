from asyncio import WindowsSelectorEventLoopPolicy
from quart import Quart, render_template, request, redirect
import asyncio
from quart_auth import (
    AuthUser, current_user, login_required, login_user, logout_user, QuartAuth
)
from UserLogin import UserLogin, createUser
from adminPanelMethods import adminControl
from servers import reverseServer1
import db

app = Quart(__name__, static_folder="www/files", template_folder="www")
app.config["SECRET_KEY"] = "iojoijoijoijjijjkjlbhyuglftdfyugf7y"
auth_manager = QuartAuth(app)
app.secret_key = "iojoijoijoijjijjkjlbhyuglftdfyugf7y"

@app.route("/", methods=["GET", "POST"])
@app.route("/Registration_user.html", methods=["GET", "POST"])
async def index():
    await db.initialize_pool()  # Инициализация пула соединений
    if request.method == "POST":
        form_data = await request.form  # Ожидаем выполнения корутины
        email = form_data['email']
        password = form_data['password']
        check = await reverseServer1.authAdmin(email, password)
        if check and check.get_id() is not None:
            user = createUser(check)  # Создание экземпляра UserLogin
            login_user(user)  # Аутентификация пользователя
            return redirect("/Main_menu.html")
        else:
            return await render_template("Registration_user.html", error="Неверный логин или пароль")

    return await render_template("Registration_user.html")


@app.route("/Main_menu.html")
@login_required
async def menu():
    return await render_template("Main_menu.html")


@app.route("/Filtering_rules.html", methods=["GET", "POST"])
@login_required
async def filter():
    if request.method == "POST":
        form_data = await request.form
        action_type = form_data["type"]
        if action_type == "mask":
            await adminControl().changeMaskMethod(1)
        elif action_type == "delete":
            await adminControl().changeMaskMethod(2)
        elif action_type == "filter":
            await adminControl().changeMaskMethod(3)
        return redirect("Filtering_rules.html")
    return await render_template("Filtering_rules.html")


@app.route("/data_sorce.html")
@login_required
async def source():
    return await render_template("data_sorce.html")

@app.route("/UserSupport.html")
@login_required
async def userSupport():
    return await render_template("UserSupport.html")

@app.route("/logout")
@login_required
async def logout():
    await logout_user()  # Выход пользователя
    return redirect("Registration_user.html")

@app.route("/Cats.html")
@login_required
async def cat():
    return await render_template("Cats.html")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    app.run(host='127.0.0.1', port=5051, debug=True)
