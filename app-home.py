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
getTab={"Country":tbe.getCountryTab,"State":tbe.getStateTab,"City":tbe.getCityTab}
application = app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
	data=getTab["Country"]()
	print(data)
	tab=render_template("tabTemp.html",columns=data["cols"],keys=data["keys"],data=data["data"])
	return render_template("locationTabs.html",sel="Country",html=tab,keys=data["keys"],keysStr=str(data["keys"]))
@app.route('/search', methods=['POST'])
def search():
	data = request.json
	tab=getTab[data["tab"]](query=data["query"])
	return (jsonify({"reply": {"auth": 1, "exe":[{"method":"fillTable","arg":render_template("tabTemp.html",columns=tab["cols"],keys=tab["keys"],data=tab["data"])},{"method":"makeOnEnters","arg":data["keys"]}]}}))


if __name__ == '__main__':
    app.secret_key = 'password'
    app.debug = True
    app.run(host='0.0.0.0',port=80,threaded=True)