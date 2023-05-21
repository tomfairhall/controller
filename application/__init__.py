from flask import Flask
from application import database
from display import Display

def init_app():
    app = Flask(__name__)

    database.init_app(app)
    display = Display(mode='s')
    display.init_app(app)

    with app.app_context():
        from . import routes
        database.init_database()
        display.init_display()
        return app