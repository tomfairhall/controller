from flask import Flask
from application import database
from controller import Display

# hacky
display = Display(mode='s')

def enter():
    display.__enter__()

def exit():
    display.__exit__(None, None, None)

def init_app():
    app = Flask(__name__)

    database.init_app(app)

    app.teardown_appcontext(exit)

    with app.app_context():
        from . import routes
        database.init_database()
        enter()
        return app