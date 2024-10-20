from flask import Blueprint, render_template, request,redirect
import json

from servers.reverseServer1 import decode

MethBP = Blueprint('Meth', __name__)

@MethBP.route('/index')
@MethBP.route('/')
def home():
    return render_template("index.html")


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
        print(form)
        return "Запрос прошел"