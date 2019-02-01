import json
from pyramid.response import Response
from apis.allergies.service import insert_allergies, fetch_allergies

def add_allergy(request):
	try:
		insert_allergies(request)
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

def get_allergy(request):
	try:
		rec =fetch_allergies(request)
	except Exception:
		return Response(
				status='404',
				body=json.dumps({'Details': 'Record Not Found'}),
				content_type='application/json; charset=UTF-8')

	return Response(
		status='200',
		body=json.dumps(rec),
		content_type='application/json; charset=UTF-8')

