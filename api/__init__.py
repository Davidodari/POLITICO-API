from flask import Flask, make_response, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os
# Setup Models
from .v1 import models
# Import blueprint - contain routes handling interaction between view and models
from .v1.views.user_view import user_api
from .v1.views.petition_view import petition_api
from .v1.views.party_view import party_api
from .v1.views.office_view import office_api
from instance.config import application_config
from .db_conn import create_tables, drop_tables
from .v2.views.user import user_api_v2
from .v2.views.office import office_api_v2
from .v2.views.parties import parties_api_v2
from .v2.views.candidate import candidate_api_v2
from .v2.views.votes import votes_api_v2
from .v2.views.results import result_api_v2


# Error Handler Methods
def page_not_found(e):
    error_response = {
        "error": "404 ERROR:REQUESTED DATA NOT FOUND",
        "status": 404
    }
    return make_response(jsonify(error_response), 404)


def method_not_allowed(e):
    error_response = {
        "error": "Performed action not allowed on resource",
        "status": 405
    }
    return make_response(jsonify(error_response), 405)


def server_error(e):
    error_response = {
        "error": "Internal Server Error",
        "status": 500
    }
    return make_response(jsonify(error_response), 500)


# configure app prerequisites
def create_app(configuration='development'):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(application_config[configuration])
    # JWT Config
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # 24 hrs to expire
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400
    JWTManager(app)
    CORS(app)
    #  Register  blueprints in app instance creation - version1
    app.register_blueprint(user_api)
    app.register_blueprint(petition_api)
    app.register_blueprint(party_api)
    app.register_blueprint(office_api)
    # Register app blue prints version 2
    create_tables()
    app.register_blueprint(user_api_v2)
    app.register_blueprint(office_api_v2)
    app.register_blueprint(parties_api_v2)
    app.register_blueprint(candidate_api_v2)
    app.register_blueprint(votes_api_v2)
    app.register_blueprint(result_api_v2)
    # Error Handler register
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(405, method_not_allowed)
    app.register_error_handler(500, server_error)
    # Return application context
    return app
