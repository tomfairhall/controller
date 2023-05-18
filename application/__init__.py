from flask import Flask
from application import database
from controller import Display

def init_app():
    app = Flask(__name__)

    database.init_app(app)

    with app.app_context():
        from . import routes
        database.init_database()
        Display(mode="s").__enter__()
        return app