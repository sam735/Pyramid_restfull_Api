import json
from pyramid.response import Response
from apis.immunization.service import insert_immunization, search_immunization


def add_immunization(request):
	try:
		insert_immunization(request)
	except Exception:
		request.db.rollback()
		return Response(
			status='500',
			body=json.dumps(
				{'Details': 'Internal server error,please try after some time'}),
			content_type='application/json; charset=UTF-8')

	return Response(
		status='201',
		body=json.dumps({'Details': 'Procedure is created'}),
		content_type='application/json; charset=UTF-8')

def fetch_immunization(request):
	try:
		rec = search_immunization(request)
	except Exception:
		return Response(
			status='500',
			body=json.dumps({'Details': 'Internal server error, please try after some time'}),
			content_type='application/json; charset=UTF-8')

	return Response(
		status='200',
		body=json.dumps(rec),
		content_type='application/json; charset=UTF-8')