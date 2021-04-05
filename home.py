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

def getCountryTab(id="",query={}):
	cols = ["countryName","countryCode","continentName","continentCode"]
	if id==None:
		qr=""
		if query!={}:
			if type(query)==str:
				q={}
				for i in cols:
					q[i]=query
				query=q
			qr=makeWhereQuery(query,cols)
		data=dbh.getTable("Mcountry,Mcontinent",cols,qr,join={"continentId":"Mcontinent.id"})
		return({"data":data,"cols":["Country Name","Country Code","Continent Name","Continent Code"],"keys":cols})