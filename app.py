from flask import Flask
from flask_session import Session
from apis.medium import medium_api
from apis.devto import devto_api
from apis.twitter import twitter_api
from apis.linkedin import linkedin_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(medium_api, url_prefix='/medium')
    app.register_blueprint(devto_api,url_prefix="/devto")
    app.register_blueprint(twitter_api,url_prefix='/twitter')
    app.register_blueprint(linkedin_api,url_prefix="/linkedin")
    app.secret_key = 'imdpKiIq0C'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config.from_object(__name__)
    Session(app)
    from routes import register_routes
    register_routes(app)

    return app
