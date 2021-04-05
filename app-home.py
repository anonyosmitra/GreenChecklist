import json
import requests
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import tabBackEnd as tbe

import arraylizer as arr
import dbHandler as dbh
import os
import requests
import timezone as tz
import ssl,socket

application = app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
	data=tbe.getCountryTab()
	tab=render_template("tabTemp.html",columns=data["cols"],keys=data["keys"],data=data["data"])
	return render_template("locationTabs.html",sel="Country",html=tab)

if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0',port=80,threaded=True)