from pyramid.response import Response
from apis.procedure.procedure_service import insert_procedure

def add_procedure(request):
	import pdb;pdb.set_trace()
	return insert_procedure(request)