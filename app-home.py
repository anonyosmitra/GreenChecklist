import json
import sys
import traceback

import requests
from flask import Flask, render_template, request, jsonify, send_file, json,flash
from flask_cors import CORS
import tabBackEnd as tbe
from werkzeug.exceptions import HTTPException, InternalServerError
from traceback import format_exception

import arraylizer as arr
import dbHandler as dbh
import os
import requests
import timezone as tz
import ssl, socket

getTab = {"Country": tbe.getCountryTab, "Region": tbe.getRegionTab, "State": tbe.getStateTab, "City": tbe.getCityTab}
newEntry = {"Country": tbe.newCountry, "Region": tbe.newRegion, "State": tbe.newState, "City": tbe.newCity}
application = app = Flask(__name__)
CORS(app)
f=open(".git/refs/heads/master", "r")
version=f.read()[:-1]
f.close()


@app.route('/home', methods=['GET'])
def barebones():
	# data=getTab["Country"]()
	return render_template("locationTabs.html", sel="Country", result="", keys=[], profile="")


# return render_template("body.html",html=render_template("locationTabs.html",sel="Country",result=tab,keys=data["keys"],profile=""))

@app.route('/', methods=['GET'])
def home():
	data = getTab["Country"]()
	tab = render_template("tabTemp.html", columns=data["cols"], keys=data["keys"], data=data["data"])
	return render_template("body.html", html=render_template("locationTabs.html", sel="Country", result=tab, keys=data["keys"], profile=""))


@app.route('/loadProfile', methods=['POST'])
def loadProfile():
	data = request.json
	edit = False
	if "edit" in data and data["edit"]:
		edit = True
	info = getTab[data["tab"]](id=data["id"], edit=edit)
	if edit:
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillProfile", "arg": render_template("profile.html", data=info["data"], edit=edit, tab=data["tab"], id=data["id"])}, {"method": "cacheProfileFields", "arg": info["col"]}, {"method": "cacheToken", "arg": info["token"]}]}}))
	else:
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillProfile", "arg": render_template("profile.html", data=info, edit=edit, tab=data["tab"], id=data["id"])}]}}))


@app.route('/UpdateSelOpts', methods=['POST'])
def UpdateSelOpts():
	data = request.json
	opts = tbe.getOptions(data["tab"], data["var"], data["val"])
	for i in opts:
		i["html"] = render_template("selOpts.html", opts=i["opts"], sel=None)
	return (jsonify({"reply": {"auth": 1, "exe": [{"method": "setSelOpts", "arg": opts}]}}))


@app.route('/search', methods=['POST'])
def search():
	data = request.json
	tab = getTab[data["tab"]](query=data["query"])
	return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillTable", "arg": render_template("tabTemp.html", columns=tab["cols"], keys=tab["keys"], data=tab["data"])}, {"method": "makeOnEnters", "arg": tab["keys"]}]}}))


@app.route('/openTab', methods=['POST'])
def openTab():
	tabName = request.json["tab"]
	tab = getTab[tabName]()
	return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillTable", "arg": render_template("tabTemp.html", columns=tab["cols"], keys=tab["keys"], data=tab["data"])}, {"method": "makeOnEnters", "arg": tab["keys"]}, {"method": "selTab", "arg": tabName}]}}))


@app.route('/addNew', methods=['POST'])
def addNew():
	data = request.json
	print(data)
	if "form" in data:
		id = newEntry[data["tab"]](data["form"], data["token"])
		if type(id) != int:
			return (jsonify({"reply": {"auth": 1, "exe": [{"method": "profileError", "arg": id}]}}))
		else:
			info = getTab[data["tab"]](id=id, edit=False)
			return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillProfile", "arg": render_template("profile.html", data=info, edit=False, tab=data["tab"], id=id)}]}}))
	else:
		info = newEntry[data["tab"]]()
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillProfile", "arg": render_template("profile.html", data=info["data"], edit=True, tab=data["tab"], id=0)}, {"method": "cacheProfileFields", "arg": info["col"]}, {"method": "cacheToken", "arg": info["token"]}]}}))


@app.route('/saveEdit', methods=['POST'])
def saveEdit():
	data = request.json
	print(data)
	id = tbe.saveEdit(data["tab"], data["form"], data["id"], data["token"])
	if type(id) != int:
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "profileError", "arg": id}]}}))
	else:
		info = getTab[data["tab"]](id=id, edit=False)
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillProfile", "arg": render_template("profile.html", data=info, edit=False, tab=data["tab"], id=id)}]}}))


@app.route('/deleteEntry', methods=['POST'])
def deleteEntry():
	data = request.json
	resp = tbe.deleteEntry(data["tab"], data["id"], data["token"])
	if resp == True:
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "fillProfile", "arg": ""}]}}))
	else:
		return (jsonify({"reply": {"auth": 1, "exe": [{"method": "profileError", "arg": resp}]}}))


"""@app.errorhandler(Exception)
def handle_exception(e):
	global version
	print(traceback.format_tb(e.__traceback__))
	print(e)
	print(version)
	return "__InternalServerError__",500"""
@app.errorhandler(404)
def http404(ex):
	# toFile(ex)
	return "Unknown Router", 404

@app.errorhandler(Exception)
def handle_exception(ex,html=False):
	global version
	print(traceback.format_tb(ex.__traceback__))
	if html:
		return ("<title></title><h1>Internal Server Error</h1><br><b>Please report to your system admin referring:<br><b>Process Id %s</b>" % (str(id))),500
	else:
		return jsonify({"reply": {"auth": 1, "reply": {"exe": [{"method": "displayError", "arg": {"msg": "Error Processing Request, Process ID: %s" % (id)}}]}}}),200

@app.route('/html', methods=['GET'])
def html():
	try:
		a = ["test"]
		flash(a)
		return a[1]
	except Exception as ex:
		return handle_exception(ex,True)
@app.route('/json', methods=['GET'])
def test():
	a = ["test"]
	flash(a)
	return a[1]




# def toFile(e)
if __name__ == '__main__':
	app.secret_key = 'password'
	app.debug = True
	print("Starting App Version: %s" % version)
	app.run(host='0.0.0.0', port=80, threaded=True)
