import sys
from asyncio import WindowsSelectorEventLoopPolicy

from flask import Flask, g
from flask_talisman import Talisman

from dbFunc import fetch_data
from serviceMethods import MethBP
from db import get_conn, initialize_pool
import asyncio

siteApp = Flask(__name__, static_folder="www/files", template_folder="www")
siteApp.config['SECRET_KEY'] = 'qWefvlbrgrotpzcv436452fvreggwF'

csp = {'default-src': "'self'"}

Talisman(siteApp, force_https=True, strict_transport_security=True, strict_transport_security_max_age=31536000)


# async def check_connections():
#     while True:
#         await asyncio.sleep(6000)
#         pool.check()





async def start_app():
    await initialize_pool()
    siteApp.run(ssl_context=('SSL/cert.pem', 'SSL/key.pem'), host="0.0.0.0", port=5000, debug=True)


siteApp.register_blueprint(MethBP)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(WindowsSelectorEventLoopPolicy())
    asyncio.run(start_app())
