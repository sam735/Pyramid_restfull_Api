import json
from pyramid.response import Response
from apis.procedure.service import insert_procedure,fetch_procedure

def add_procedure(request):
	#import pdb;pdb.set_trace()
	try:
		insert_procedure(request)
	except Exception:
		request.db.rollback()
		return Response(
        status='500',
        body=json.dumps({'Details': 'Internal server error,please try after some time'}),
        content_type='application/json; charset=UTF-8')

	return Response(
        status='201',
        body=json.dumps({'Details': 'Procedure is created'}),
        content_type='application/json; charset=UTF-8')

def search_procedure(request):
        import pdb;pdb.set_trace()
        try:
                rec = fetch_procedure(request)
        except Exception:
                return Response(
                        status='404',
                        body=json.dumps({'Details': 'Record Not Found'}),
                        content_type='application/json; charset=UTF-8')

        return Response(
        status='201',
        body=json.dumps(rec),
        content_type='application/json; charset=UTF-8')
