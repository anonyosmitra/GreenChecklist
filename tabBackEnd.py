import dbHandler as dbh
import os
import requests
import timezone as tz


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
	data=con.getTable("M"+get,["M"+get+".id",get+"Name"],where,columnNames=["id","name"],ext="order by "+get+"Name")
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
			data={"data": data, "col": ["countryName", "countryCode", "continentId"]}
		else:
			data = con.getTable("Mcountry,Mcontinent", ["countryName", "countryCode", "continentName"], {"Mcountry.id": id},join={"continentId": "Mcontinent.id"})[0]
			data = [{"name": "Name", "value": data["countryName"]}, {"name": "Country Code", "value": data["countryCode"]}, {"name": "Continent", "value": data["continentName"]}]
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
		data = con.getTable("Mstate,Mcountry,Mcontinent", ["Mstate.id"] + cols, qr, join={"countryId": "Mcountry.id", "continentId": "Mcontinent.id"}, ext="order by stateName", columnNames=["id"] + cols)
		data = {"data": data, "cols": ["State", "Abbr", "Country", "Continent"], "keys": cols}
	else:
		if edit:
			data = con.getTable("Mstate,Mcountry", ["stateName","stateSName","regionId","countryId", "Mcountry.continentId"], {"Mstate.id": id},join={"Mcountry.id":"countryId"},columnNames=["stateName","stateSName","regionId","countryId", "continentId"])[0]
			data = [{"name": "Name", "value": data["stateName"],"var":"stateName"}, {"name": "Abbr", "value": data["stateSName"],"var":"stateSName"}, {"name": "Region", "value": data["regionId"],"var":"regionId","opts": makeSelectOpts("region" ,"country" ,data["countryId"] ,con=con)}, {"name": "Country","var":"countryId", "value": data["countryId"],"opts": makeSelectOpts("country" ,"continent" ,data["continentId"] ,con=con)}, {"name": "Continent","var":"continentId", "value": data["continentId"],"opts":makeSelectOpts("continent",con=con)}]
			data = {"data": data, "col": ["stateName","stateSName","regionId","countryId", "continentId"]}
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
		info += [{"var": sel[0].lower()+"Id", "opts": makeSelectOpts(sel[0].lower(), var, val, con) + [{"name": "Select %s" % (sel[0])}]}]
		if kilcon:
			con.close()
		if len(sel)>1:
			for i in range(1,len(sel)):
				info += [{"var": sel[i].lower()+"Id", "opts":[{"name":"Select %s First"%(sel[0])}]}]
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
		data = con.getTable("Mcity,Mstate,Mcountry,Mcontinent", ["Mcity.id"] + cols, qr, join={"stateId": "Mstate.id", "Mstate.countryId": "Mcountry.id", "continentId": "Mcontinent.id"}, ext="order by cityName", columnNames=["id"] + cols)
		data = {"data": data, "cols": ["City", "Abbr", "State", "Country", "Continent"], "keys": cols}
	if kilcon:
		con.close()
	return data
