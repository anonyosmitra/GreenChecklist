def getOptions(tab):
	sel = ['Continent', 'Country', 'Region', 'State',"City"]
	sel=sel[:sel.index(tab.capitalize())]
	print(sel)
	j={}
	tabs=[]
	for i in range(0,len(sel)-1):
		j["M"+sel[i].lower()+".id"]="M"+sel[i+1].lower()+"."+sel[i].lower()+"Id"
		tabs+=["M"+sel[i].lower()]
	print(j)
	print(",".join(tabs))
getOptions("country")
getOptions("city")