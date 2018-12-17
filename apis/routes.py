from apis.procedure.controller import add_procedure

def includeme(config):
	config.add_route('insert_procedure', '/v1.0/procedure')
	config.add_view(add_procedure, renderer="json", route_name='insert_procedure')