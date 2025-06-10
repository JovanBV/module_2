def register_api(app, API, name):
    item = API.as_view(f'{name}')
    app.add_url_rule(f'/{name}/<int:id>', view_func=item, methods=['GET', 'DELETE', 'PATCH'])
    app.add_url_rule(f'/{name}', view_func=item, methods=['POST', 'GET'])