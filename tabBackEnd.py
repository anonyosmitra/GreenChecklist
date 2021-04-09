import dbHandler as dbh
import os
import requests
import timezone as tz
import datetime as dt
zones=[]
for i in tz.tzList:
	zones+=[{"id":i,"name":i}]
def requestToken(con=None,id=None,):
	kilcon = False
	resp=0
	if con == None:
		con = dbh.Connect()
		kilcon = True
	con.deleteFromTable("formHandler", dbh.appendQuery("time>\"%0\"", [dt.datetime.now() + dt.timedelta(minutes=20)]))
	if id==None:
		resp=con.insertIntoTable("formHandler",{"memo":"ok"},returnId=True)
	else:
		resp=[False,True][con.deleteFromTable("formHandler",{"id":id},returnCount=True)]
	if kilcon:
		con.close()
	return resp
def makeWhereQuery(query, cols=None, gate="or"):
	qr = ""
	if query == {}:
		return qr
	else:
		for i in query:
			if cols != None and i in cols:
				qr += (dbh.appendQuery("%0 like \"%1?\" %s ", [i, query[i]]) % (gate)).replace("?", "%")
			elif cols == None:
				qr += (dbh.appendQuery("%0 like \"%1?\" %s ", [i, query[i]]) % (gate)).replace("?", "%")
		if len(qr) > 0:
			qr = qr[:-(len(gate) + 2)]
		return qr


# (get="country",where="continent",id=1)=[{"id"=4,"name":"Algeria"},{"id":7,"name":"Angola"}...]
def makeSelectOpts(get, where=None,id=None, con=None):
	kilcon = False
	if con == None:
		con = dbh.Connect()
		kilcon = True
	if where==None:
		where=""
	else:
		where={where + "Id": id}
	data=con.getTable(dbh.appendQuery("M%0",[get.lower()]),[dbh.appendQuery("M%0.id",[get.lower()]),dbh.appendQuery("%0Name",[get.lower()])],where,columnNames=["id","name"],ext=dbh.appendQuery("order by %0Name",[get]))
	if kilcon:
		con.close()
	return data

def getCountryTab(id=None, query={}, con=None, edit=False):
	kilcon = False
	if con == None:
		con = dbh.Connect()
		kilcon = True
	if id == None:
		cols = ["countryName", "countryCode", "continentName", "continentCode"]
		qr = ""
		if query != {}:
			if type(query) == str:
				q = {}
				for i in cols:
					q[i] = query
				query = q
			qr = makeWhereQuery(query, cols)
			qr = "(%s)" % (qr)
		data = con.getTable("Mcountry,Mcontinent", ["Mcountry.id"] + cols, qr, join={"continentId": "Mcontinent.id"}, ext="order by countryName", columnNames=["id"] + cols)
		data = {"data": data, "cols": ["Country", "Country Code", "Continent", "Continent Code"], "keys": cols}
	else:
		if edit:
			data = con.getTable("Mcountry", ["countryName", "countryCode", "continentId"], {"Mcountry.id": id})[0]
			data = [{"name": "Name", "value": data["countryName"],"var":"countryName"}, {"name": "Country Code", "value": data["countryCode"],"var":"countryCode"}, {"name": "Continent", "value": data["continentId"],"var":"continentId","opts":makeSelectOpts("continent",con=con)}]
			data={"data": data, "col": ["countryName", "countryCode", "continentId"],"token":requestToken(con)}
		else:
			data = con.getTable("Mcountry,Mcontinent", ["countryName", "countryCode", "continentName"], {"Mcountry.id": id},join={"continentId": "Mcontinent.id"})[0]
			data = [{"name": "Name", "value": data["countryName"]}, {"name": "Country Code", "value": data["countryCode"]}, {"name": "Continent", "value": data["continentName"]}]
	if kilcon:
		con.close()
	return data

def getRegionTab(id=None, query={}, con=None, edit=False):
	kilcon = False
	if con == None:
		con = dbh.Connect()
		kilcon = True
	if id == None:
		cols = ["regionName", "regionSName", "countryName", "continentName"]
		qr = ""
		if query != {}:
			if type(query) == str:
				q = {}
				for i in cols:
					q[i] = query
				query = q
			qr = makeWhereQuery(query, cols)
			qr = "(%s)" % (qr)
		data = con.getTable("Mregion,Mcountry,Mcontinent", ["Mregion.id"] + cols, qr, join={"countryId": "Mcountry.id", "continentId": "Mcontinent.id"}, ext="order by regionName", columnNames=["id"] + cols)
		data = {"data": data, "cols": ["Region", "Abbr", "Country", "Continent"], "keys": cols}
	else:
		if edit:
			data = con.getTable("Mregion,Mcountry", ["regionName", "regionSName", "countryId", "Mcountry.continentId"], {"Mregion.id": id}, join={"Mcountry.id": "countryId"}, columnNames=["regionName", "regionSName", "countryId", "continentId"])[0]
			data = [{"name": "Name", "value": data["regionName"], "var": "regionName"}, {"name": "Abbr", "value": data["regionSName"], "var": "regionSName"}, {"name": "Country", "var": "countryId", "value": data["countryId"], "opts": makeSelectOpts("country", "continent", data["continentId"], con=con)}, {"name": "Continent", "var": "continentId", "value": data["continentId"], "opts": makeSelectOpts("continent", con=con)}]
			data = {"data": data, "col": ["regionName", "regionSName", "countryId", "continentId"],"token":requestToken(con)}
		else:
			data = con.getTable("Mregion,Mcountry,Mcontinent", ["regionName", "regionSName", "countryName", "continentName"], where={"Mregion.id": id}, join={ "Mregion.countryId": "Mcountry.id", "Mcountry.continentId": "Mcontinent.id"})[0]
			data = [{"name": "Name", "value": data["regionName"]}, {"name": "Abbr", "value": data["regionSName"]}, {"name": "Country", "value": data["countryName"]}, {"name": "Continent", "value": data["continentName"]}]
	if kilcon:
		con.close()
	return data
def getStateTab(id=None, query={}, con=None, edit=False):
	kilcon = False
	if con == None:
		con = dbh.Connect()
		kilcon = True
	if id == None:
		cols = ["stateName", "stateSName", "countryName", "continentName"]
		qr = ""
		if query != {}:
			if type(query) == str:
				q = {}
				for i in cols:
					q[i] = query
				query = q
			qr = makeWhereQuery(query, cols)
			qr = "(%s)" % (qr)
		data = con.getTable("Mstate,Mregion,Mcountry,Mcontinent", ["Mstate.id"] + cols, qr, join={"regionID":"Mregion.id","countryId": "Mcountry.id", "continentId": "Mcontinent.id"}, ext="order by stateName", columnNames=["id"] + cols)
		data = {"data": data, "cols": ["State", "Abbr", "Country", "Continent"], "keys": cols}
	else:
		if edit:
			data = con.getTable("Mstate,Mregion,Mcountry", ["stateName","stateSName","regionId","countryId", "continentId"], {"Mstate.id": id},join={"Mregion.id":"regionId","Mcountry.id":"countryId"},columnNames=["stateName","stateSName","regionId","countryId", "continentId"])[0]
			data = [{"name": "Name", "value": data["stateName"],"var":"stateName"}, {"name": "Abbr", "value": data["stateSName"],"var":"stateSName"}, {"name": "Region", "value": data["regionId"],"var":"regionId","opts": makeSelectOpts("region" ,"country" ,data["countryId"] ,con=con)}, {"name": "Country","var":"countryId", "value": data["countryId"],"opts": makeSelectOpts("country" ,"continent" ,data["continentId"] ,con=con)}, {"name": "Continent","var":"continentId", "value": data["continentId"],"opts":makeSelectOpts("continent",con=con)}]
			data = {"data": data, "col": ["stateName","stateSName","regionId","countryId", "continentId"],"token":requestToken(con)}
		else:
			data = con.getTable("Mstate,Mregion,Mcountry,Mcontinent", ["stateName","stateSName","regionName","countryName","continentName"], where={"Mstate.id": id}, join={"Mstate.regionId":"Mregion.id","Mregion.countryId":"Mcountry.id","Mcountry.continentId": "Mcontinent.id"})[0]
			data = [{"name": "Name", "value": data["stateName"]},{"name": "Abbr", "value": data["stateSName"]},{"name": "Region", "value": data["regionName"]},{"name": "Country", "value": data["countryName"]}, {"name": "Continent", "value": data["continentName"]}]
	if kilcon:
		con.close()
	return data


def getOptions(tab,var,val,con=None):
	kilcon = False
	sel = ['Continent', 'Country', 'Region', 'State', 'City']
	var=var[:-2]
	sel = sel[sel.index(var.capitalize()) + 1:sel.index(tab.capitalize())]
	info=[]
	if len(sel)>0:
		if con == None:
			con = dbh.Connect()
			kilcon = True
		info += [{"var": dbh.appendQuery("%0Id",[sel[0].lower()]), "opts": [{"name": "Select %s" % (sel[0])}]+makeSelectOpts(sel[0].lower(), var, val, con)}]
		if kilcon:
			con.close()
		if len(sel)>1:
			for i in range(1,len(sel)):
				info += [{"var": dbh.appendQuery("%0Id",[sel[i].lower()]), "opts":[{"name":"Select %s First"%(sel[0])}]}]
	return info
def getCityTab(id=None, query={}, con=None, edit=False):
	kilcon = False
	if con == None:
		con = dbh.Connect()
		kilcon = True
	if id == None:
		cols = ["cityName", "citySName", "stateName", "countryName", "continentName"]
		qr = ""
		if query != {}:
			if type(query) == str:
				q = {}
				for i in cols:
					q[i] = query
				query = q
			qr = makeWhereQuery(query, cols)
			qr = "(%s)" % (qr)
		data = con.getTable("Mcity,Mstate,Mregion,Mcountry,Mcontinent", ["Mcity.id"] + cols, qr, join={"regionId":"Mregion.id","stateId": "Mstate.id", "countryId": "Mcountry.id", "continentId": "Mcontinent.id"}, ext="order by cityName", columnNames=["id"] + cols)
		data = {"data": data, "cols": ["City", "Abbr", "State", "Country", "Continent"], "keys": cols}
	else:
		if edit:
			data = con.getTable("Mcity,Mstate,Mregion,Mcountry", ["cityName", "citySName", "stateId", "regionId", "countryId", "continentId","timezone"], {"Mcity.id": id}, join={"stateId":"Mstate.id","Mregion.id":"regionId","Mcountry.id": "countryId"}, columnNames=["cityName", "citySName", "stateId", "regionId", "countryId", "continentId","timezone"])[0]
			data = [{"name": "Name", "value": data["cityName"], "var": "cityName"}, {"name": "Abbr", "value": data["citySName"], "var": "citySName"}, {"name": "State", "value": data["stateId"], "var": "stateId", "opts": makeSelectOpts("state", "region", data["regionId"], con=con)}, {"name": "Region", "value": data["regionId"], "var": "regionId", "opts": makeSelectOpts("region", "country", data["countryId"], con=con)}, {"name": "Country", "var": "countryId", "value": data["countryId"], "opts": makeSelectOpts("country", "continent", data["continentId"], con=con)}, {"name": "Continent", "var": "continentId", "value": data["continentId"], "opts": makeSelectOpts("continent", con=con)},{"name": "Timezone", "var": "timezone", "value": data["timezone"], "opts": zones}]
			data = {"data": data, "col": ["cityName", "citySName", "stateId", "regionId", "countryId", "continentId","timezone"],"token":requestToken(con)}
		else:
			data = con.getTable("Mcity,Mstate,Mregion,Mcountry,Mcontinent", ["cityName","citySName","stateName", "regionName", "countryName", "continentName","timezone"], where={"Mcity.id": id}, join={"stateId": "Mstate.id","regionId": "Mregion.id", "countryId": "Mcountry.id", "continentId": "Mcontinent.id"})[0]
			data = [{"name": "Name", "value": data["cityName"]}, {"name": "Abbr", "value": data["citySName"]},{"name": "State", "value": data["stateName"]}, {"name": "Region", "value": data["regionName"]}, {"name": "Country", "value": data["countryName"]}, {"name": "Continent", "value": data["continentName"]},{"name": "Timezone", "value": data["timezone"]}]
	if kilcon:
		con.close()
	return data
def checkValidity(id,data,tab,con=None):
	kilcon = False
	if con == None:
		con = dbh.Connect()
		kilcon = True
	resp=True
	qr={}
	for i in data:
		if data[i]=="" or data[i]==None:
			resp = "Empty value detected!"
		if i[-4:]=="Code":
			if len(con.getTable(dbh.appendQuery("M%0",[i[:-4]]),["id"],con.appendQuery("%0=\"%1\" and id!=%2",[i,data[i],id])))>0:
				resp="%s code already exists and must be unique!"%(i[:-4].capilatize())
	if kilcon:
		con.close()
	return resp
def newCountry(form=None,token=None):
	if form==None:
		data = [{"name": "Name", "value": "", "var": "countryName"}, {"name": "Country Code", "value": "", "var": "countryCode"}, {"name": "Continent", "value": 0, "var": "continentId", "opts": [{"name":"Select Continent"}]+makeSelectOpts("continent")}]
		data = {"data": data, "col": ["countryName", "countryCode", "continentId"],"token":requestToken()}
		return data
	else:
		con=dbh.Connect()
		id=checkValidity(0,form,"Country",con)
		if id==True:
			if requestToken(con,token):
				cols=con.desc("Mcountry",["name"])
				ins={}
				for i in cols:
					if i["name"] in form:
						ins[i["name"]]=form[i["name"]]
				id=con.insertIntoTable("Mcountry",ins,returnId=True)
		con.close()
		return id

def newRegion(form=None,token=None):
	if form == None:
		data = [{"name": "Name", "value": "", "var": "regionName"}, {"name": "Abbr", "value": "", "var": "regionSName"}, {"name": "Country", "var": "countryId", "value": 0, "opts": [{"name":"Select Continent First"}]}, {"name": "Continent", "var": "continentId", "value": 0, "opts": [{"name":"Select Continent"}]+makeSelectOpts("continent")}]
		data = {"data": data, "col": ["regionName", "regionSName", "countryId", "continentId"], "token": requestToken()}
		return data
	else:
		con=dbh.Connect()
		id=checkValidity(0,form,"Region",con)
		if id==True:
			if requestToken(con,token):
				cols=con.desc("Mregion",["name"])
				ins={}
				for i in cols:
					if i["name"] in form:
						ins[i["name"]]=form[i["name"]]
				id=con.insertIntoTable("Mregion",ins,returnId=True)
		con.close()
		return id
def newState(form=None,token=None):
	if form == None:
		data = [{"name": "Name", "value": "", "var": "stateName"}, {"name": "Abbr", "value": "", "var": "stateSName"}, {"name": "Region", "value": 0, "var": "regionId", "opts": [{"name":"Select Continent First"}]}, {"name": "Country", "var": "countryId", "value": 0, "opts": [{"name":"Select Continent First"}]}, {"name": "Continent", "var": "continentId", "value": 0, "opts": [{"name":"Select Continent"}]+makeSelectOpts("continent")}]
		data = {"data": data, "col": ["stateName", "stateSName", "regionId", "countryId", "continentId"], "token": requestToken()}
		return data
	else:
		con=dbh.Connect()
		id=checkValidity(0,form,"State",con)
		if id==True:
			if requestToken(con,token):
				cols=con.desc("Mstate",["name"])
				ins={}
				for i in cols:
					if i["name"] in form:
						ins[i["name"]]=form[i["name"]]
				id=con.insertIntoTable("Mstate",ins,returnId=True)
		con.close()
		return id
def newCity(form=None,token=None):
	if form == None:
		data = [{"name": "Name", "value": "", "var": "cityName"}, {"name": "Abbr", "value": "", "var": "citySName"}, {"name": "State", "value": 0, "var": "stateId", "opts": [{"name":"Select Continent First"}]}, {"name": "Region", "value": 0, "var": "regionId", "opts": [{"name":"Select Continent First"}]}, {"name": "Country", "var": "countryId", "value": 0, "opts":  [{"name":"Select Continent First"}]}, {"name": "Continent", "var": "continentId", "value": 0, "opts": [{"name":"Select Continent"}]+makeSelectOpts("continent")}, {"name": "Timezone", "var": "timezone", "value": 0, "opts": [{"name":"Select Timezone"}]+zones}]
		data = {"data": data, "col": ["cityName", "citySName", "stateId", "regionId", "countryId", "continentId", "timezone"], "token": requestToken()}
		return data
	else:
		con=dbh.Connect()
		id=checkValidity(0,form,"City",con)
		if id==True:
			if requestToken(con,token):
				cols=con.desc("Mcity",["name"])
				ins={}
				for i in cols:
					if i["name"] in form:
						ins[i["name"]]=form[i["name"]]
				id=con.insertIntoTable("Mcity",ins,returnId=True)
		con.close()
		return id
def saveEdit(tab,form,id,token):
	con = dbh.Connect()
	resp= checkValidity(0, form, tab, con)
	print(resp)
	if resp == True:
		print("Yes")
		if requestToken(con,token):
			print("Valid")
			cols = con.desc(dbh.appendQuery("M%0",[tab.lower()]),["name"])
			ins = {}
			for i in cols:
				if i["name"] in form:
					ins[i["name"]] = form[i["name"]]
			con.updateTable(dbh.appendQuery("M%0",[tab.lower()]), ins,{"id":id})
			resp=id
		else:
			print("Invalid")
	else:
		print("No")
	con.close()
	return resp
def deleteEntry(tab, id,token):
	con = dbh.Connect()
	sel = ['Country', 'Region', 'State', 'City']
	resp="Invalid Table"
	if tab in sel:
		resp = "ok"
		if sel.index(tab.capitalize()) + 1 < len(sel):
			if len(con.getTable(dbh.appendQuery("M%0",[sel[sel.index(tab.capitalize()) + 1].lower()]),["id"],{dbh.appendQuery("%0Id",[tab]):id}))>0:
				resp = dbh.appendQuery("Selected %0 has dependent entries", [tab.lower()])
				if requestToken(con,token):
					con.deleteFromTable(dbh.appendQuery("M%0",[tab.lower()]),{"id":id})
					resp=True
					print("deleted")
				else:
					print("failed")
	con.close()
	return resp

