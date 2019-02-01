from apis.procedure.controller import add_procedure, search_procedure


def includeme(config):
    config.add_route('insert_procedure', 'api/v1.0/procedures',
                     request_method="POST")
    config.add_view(add_procedure, renderer="json",
                    route_name='insert_procedure')
    config.add_route('fetch_procedure', 'api/v1.0/procedures',
                     request_method="GET")
    config.add_view(search_procedure, renderer="json",
                    route_name='fetch_procedure')