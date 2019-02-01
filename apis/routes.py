from apis.procedure.controller import add_procedure, search_procedure
from apis.allergies.controller import add_allergy,get_allergy
from apis.problems.controller import add_problem,get_problem

def includeme(config):
	import pdb; pdb.set_trace()
	config.add_route('insert_procedure', 'api/v1.0/procedures',request_method="POST")
	config.add_view(add_procedure, renderer="json", route_name='insert_procedure')
	config.add_route('fetch_procedure', 'api/v1.0/procedures',request_method="GET")s
	config.add_view(search_procedure, renderer="json", route_name='fetch_procedure')
	# config.add_route('remove_procedure', 'api/v1.0/procedures',request_method="GET")
	# config.add_view(delete_procedure, renderer="json", route_name='remove_procedure')
	config.add_route('insert_allergies', 'api/v1.0/allergies',request_method="POST")
	config.add_view(add_allergy, renderer="json", route_name="insert_allergies")
	config.add_route('fetch_allergies', 'api/v1.0/allergies',request_method="GET")
	config.add_view(get_allergy, renderer="json", route_name="fetch_allergies")
	config.add_route('insert_problems', 'api/v1.0/problems',request_method="POST")
	config.add_view(add_problem, renderer="json", route_name="insert_problems")
	config.add_route('fetch_problems', 'api/v1.0/problems',request_method="GET")
	config.add_view(get_problem, renderer="json", route_name="fetch_problems")