from flask import Flask, g
from flask_talisman import Talisman

from consts import portC1
from serviceMethods import MethBP

siteApp = Flask(__name__, static_folder="www/files", template_folder="www")
siteApp.config['SECRET_KEY'] = 'qWefvlbrgrotpzcv436452fvreggwF'

csp = {'default-src': "'self'"}

Talisman(siteApp, force_https=True, strict_transport_security=True, strict_transport_security_max_age=31536000)


def start_app():
    siteApp.run(ssl_context=('SSL/cert.pem', 'SSL/key.pem'), host="0.0.0.0", port=portC1, debug=True)


siteApp.register_blueprint(MethBP)

if __name__ == "__main__":
    start_app()
