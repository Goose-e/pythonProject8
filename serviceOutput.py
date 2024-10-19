from flask import Flask
from flask_talisman import Talisman

siteApp = Flask(__name__, static_folder="www/files", template_folder="www")
siteApp.config['SECRET_KEY'] = 'qWefvlbrgrotpzcv436452fvreggwF'

csp = { 'default-src': "'self'" }


Talisman(siteApp, force_https=True, strict_transport_security=True, strict_transport_security_max_age=31536000)



from serviceMethods import MethBP

siteApp.register_blueprint(MethBP)

if __name__ == "__main__":
    siteApp.run(ssl_context=('SSL/cert.pem', 'SSL/key.pem'))
    siteApp.run(host="0.0.0.0",port=5000,debug=True)