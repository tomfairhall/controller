from flask import Flask
from application import database

def init_app():
    app = Flask(__name__)

    database.init_app(app)

    with app.app_context():
        from . import routes
        database.init_database()

        return app