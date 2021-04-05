import json
import requests
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

import arraylizer as arr
import dbHandler as dbh
import hk
import os
import requests
import timezone as tz
import websocket,ssl,socket

application = app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
	return("<h1>HELLO WORLD!</h1>")

if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0',port=80,threaded=True)