from flask import Blueprint, render_template, request, jsonify
import json

MethBP = Blueprint('Meth', __name__)


@MethBP.route('/index')
@MethBP.route('/')
def home():
    return render_template("Service.html")


@MethBP.route('/pingTest', methods=["POST"])
def ping():
    if request.method == 'POST':
        form = json.loads(request.data.decode())
        print(form['ping'])
        return "Запрос прошел"


@MethBP.route('/userPingTest', methods=["POST"])
def userPing():
    if request.method == 'POST':
        form = json.loads(request.json)
        with open("www/files/js/datatest.log", "a", encoding="utf-8") as file:
            file.write(f'{{"Endpoint": "{form["Endpoint"]}", "Message": "{form["Message"]}", "SupportLevel": "{form["SupportLevel"]}", "Timestamp": "{form["Timestamp"]}"}}\n')
        return "Запрос прошел"


@MethBP.route('/datatest.json', methods=["GET", "POST"])
def datajson():
    list = []
    with open("www/files/js/datatest.log", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            list.append(line)
    return jsonify({"Message": list})  # Return the list as part of the Message key
