from flask import Flask, render_template
from config import Config


def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config.from_object(Config)
    from . import auth
    from chat import flask_chat
    app.register_blueprint(flask_chat.bp)
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('base.html')

    return app
