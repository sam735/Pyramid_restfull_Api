from apis.problems.services import insert_problems, fetch_problems
from pyramid.response import Response
import json


def add_problem(request):

    try:
        insert_problems(request)

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


def get_problem(request):
    try:
        rec = fetch_problems(request)
    except Exception:
        return Response(
                status='404',
                body=json.dumps({'Details': 'Record Not Found'}),
                content_type='application/json; charset=UTF-8')

    return Response(
        status='200',
        body=json.dumps(rec),
        content_type='application/json; charset=UTF-8')