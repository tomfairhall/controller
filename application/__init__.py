from flask import Flask
from application import database
from controller import Display

def init_app():
    app = Flask(__name__)

    database.init_app(app)

    with app.app_context(), Display('s'):
        from . import routes

        database.init_database()
        Display('s')
        return app