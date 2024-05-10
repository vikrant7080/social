from flask import request


def register_routes(app):
    @app.route('/', methods=['GET', 'POST'])
    def hello():
        if request.method == 'GET':
            return "Hello"
