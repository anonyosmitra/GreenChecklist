import dbHandler as dbh
import os
import requests
import timezone as tz
def makeWhereQuery(query,cols=None,gate="or"):
	qr=""
	if query=={}:
		return qr
	else:
		for i in query:
			if cols!=None and i in cols:
				qr += (dbh.appendQuery("%0 like \"%1?\" %s ",[i,query[i]])%(gate)).replace("?","%")
			elif cols==None:
				qr += (dbh.appendQuery("%0 like \"%1?\" %s ", [i, query[i]]) % (gate)).replace("?", "%")
		if len(qr)>0:
			qr=qr[:-(len(gate) + 2)]
		return qr

def getCountryTab(id=None,query={}):
	if id==None:
		cols = ["countryName", "countryCode", "continentName", "continentCode"]
		qr=""
		if query!={}:
			if type(query)==str:
				q={}
				for i in cols:
					q[i]=query
				query=q
			qr=makeWhereQuery(query,cols)
			qr="(%s)" % (qr)
		data=dbh.getTable("Mcountry,Mcontinent",cols,qr,join={"continentId":"Mcontinent.id"},ext="order by countryName")
		return({"data":data,"cols":["Country","Country Code","Continent","Continent Code"],"keys":cols})


def getStateTab(id=None,query={}):
	if id==None:
		cols = ["stateName","stateSName", "countryName", "continentName"]
		qr=""
		if query!={}:
			if type(query)==str:
				q={}
				for i in cols:
					q[i]=query
				query=q
			qr=makeWhereQuery(query,cols)
			qr = "(%s)" % (qr)
		data=dbh.getTable("Mstate,Mcountry,Mcontinent",cols,qr,join={"countryId":"Mcountry.id","continentId":"Mcontinent.id"},ext="order by stateName")
		return({"data":data,"cols":["State","Abbr", "Country", "Continent"],"keys":cols})



def getCityTab(id=None,query={}):
	if id==None:
		cols = ["cityName","citySName","stateName", "countryName", "continentName"]
		qr=""
		if query!={}:
			if type(query)==str:
				q={}
				for i in cols:
					q[i]=query
				query=q
			qr=makeWhereQuery(query,cols)
			qr = "(%s)" % (qr)
		data=dbh.getTable("Mcity,Mstate,Mcountry,Mcontinent",cols,qr,join={"stateId":"Mstate.id","Mstate.countryId":"Mcountry.id","continentId":"Mcontinent.id"},ext="order by cityName")
		return({"data":data,"cols":["City", "Abbr", "State", "Country", "Continent"],"keys":cols})