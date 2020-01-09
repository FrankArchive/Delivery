from flask import Flask
from credentials import credentials
from transport import transport
from shop import shop
from config import config

app = Flask(__name__)
app.register_blueprint(credentials, url_prefix='/creds')
app.register_blueprint(transport, url_prefix='/')
app.register_blueprint(shop, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
