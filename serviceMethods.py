from flask import Blueprint, render_template, request
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
            file.write(str(form))
            file.write("\n")
        return "Запрос прошел"

@MethBP.route('/datatest.json', methods=["GET", "POST"])
def datajson():
    list = []
    with open("www/files/js/datatest.log", "r", encoding="utf-8") as file:
        lines = file.readlines()
        for line in lines:
            item = {"Message": line.strip()}  # Process each line into a dict
            list.append(item)
    return json.dumps({"Message": list})  # Return the list as part of the Message key

