def getOptions(tab,var):
	sel = ['Continent', 'Country', 'Region', 'State', 'City']
	i = sel.index(var.capitalize()) + 1
	e = sel.index(tab.capitalize())
	sel=sel[i:e]
	print(sel)
getOptions("country","continent")
getOptions("city","continent")