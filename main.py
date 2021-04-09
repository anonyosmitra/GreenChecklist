def getOptions(tab):
	sel = ['Country', 'Region', 'State', 'City']
	if sel.index(tab)+1 < len(sel):
		print(sel[sel.index(tab)+1 ])
getOptions("Country")
getOptions("Region")
getOptions("State")
getOptions("City")