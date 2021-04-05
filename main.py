import dbHandler as dbh
print dbh.getTable("Mcity,Mstate,Mcountry,Mcontinent",["cityName","stateName","countryName","continentName"],"cityName=\"Bengaluru\"",{"stateId":"Mstate.id","Mstate.countryId":"Mcountry.id","continentId":"Mcontinent.id"})
con=dbh.Connect()
print con.getTable("Mcity,Mstate,Mcountry,Mcontinent",["cityName","stateName","countryName","continentName"],"cityName=\"Bengaluru\"",{"stateId":"Mstate.id","Mstate.countryId":"Mcountry.id","continentId":"Mcontinent.id"})
con.close()