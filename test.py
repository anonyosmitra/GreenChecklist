import traceback

def test():
	try:
		a = ["test"]
		return a[1]
	except Exception as ex:
		print(ex.__traceback__)
		print(traceback.format_tb(ex.__traceback__))
		print(traceback.format_tb(ex.__cause__))
	print("Ended")
test()