from flask import Flask
from application import database
from controller import Display

def init_app():
    app = Flask(__name__)

    database.init_app(app)
    display = Display(mode='s')

    #app.teardown_appcontext(display.__exit__)

    with app.app_context(), display:
        from . import routes
        database.init_database()
        #display.__enter__()
        return app