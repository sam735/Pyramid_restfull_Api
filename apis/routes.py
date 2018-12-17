from apis.procedure.controller import add_procedure

def includeme(config):
	config.add_route('insert_procedure', 'api/v1.0/procedures')
	config.add_view(add_procedure, renderer="json", route_name='insert_procedure')