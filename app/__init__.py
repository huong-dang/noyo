from flask import Flask, Blueprint
from flask_restplus import Api
from ma import ma
from db import db
from resources.person import Person, PersonsList, person_ns
from marshmallow import ValidationError
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    ma.init_app(app)

    bluePrint = Blueprint('api', __name__, url_prefix='/api')
    api = Api(bluePrint, doc='/doc', title='Sample Flask-RestPlus Application')
    app.register_blueprint(bluePrint)
    api.add_namespace(person_ns)

    @app.before_first_request
    def create_tables():
        db.create_all()

    person_ns.add_resource(Person, '/<id>')
    person_ns.add_resource(PersonsList, '')

    return app