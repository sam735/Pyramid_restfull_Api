from dateutil import parser
import json
import ast

class DictToObject(object):
	import pdb;pdb.set_trace()
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

	else:
		return parser.parse(str)

def to_json_obj(obj):
	import pdb;pdb.set_trace()
	l = []
	for i in range(len(obj)):
		obj_tup = obj[i].json_payload
		obj_str = ast.literal_eval(obj_tup)
		l.append(obj_str)
	return l




