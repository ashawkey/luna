import os
import time
import glob
from datetime import datetime

from flask_cors import CORS
from flask import Flask, request, jsonify

import route


app = Flask(__name__, instance_relative_config=True)
CORS(app)

app.config.from_object('config')

app.register_blueprint(route.bp)


if __name__ == "__main__":
    #app.run("0.0.0.0", 5000, ssl_context=('cert.pem', 'key.pem'))
    app.run("127.0.0.1", 8002)
