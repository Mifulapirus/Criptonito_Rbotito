def convertFromUnicode(input):
	if isinstance(input, dict):
		return {convertFromUnicode(key): convertFromUnicode(value) for key, value in input.iteritems()}
	elif isinstance(input, list):
		return [convertFromUnicode(element) for element in input]
	elif isinstance(input, unicode):
		val = input.encode('utf-8')
		try:
			return float(val)
		except:
			return val
	else:
		return input