from flask import Flask
from application import database
from controller import Display

# hacky
def enter(display: Display):
    display.__enter__()

def exit(display: Display):
    display.__exit__(None, None, None)

def init_app():
    app = Flask(__name__)

    database.init_app(app)
    display = Display(mode='s')

    app.teardown_appcontext(exit(display))

    with app.app_context():
        from . import routes
        database.init_database()
        enter(display)
        return app