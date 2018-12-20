from dateutil import parser

class DictToObject(object):
	def __init__(self, d):
		self.__dict__ = d

	def __getattr__(self, item):
		return None

def return_lower_case_of_string(str):
	return str.lower()



def convertStringToDateTime(str):
	try:
		return parser.parse(str)
	except Exception:
		return None

