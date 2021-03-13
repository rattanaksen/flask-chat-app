from flask import Flask, render_template, session
from flask_mail import Mail, Message


def init_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['DEBUG'] = True
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_DEFAULT_SENDER'] = 'sanmurria@gmail.com'
    app.config['MAIL_USERNAME'] = 'sanmurria'
    app.config['MAIL_PASSWORD'] = "g3&x'AdrM!#S"

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/forgot_password')
    def forgot_password():
        return render_template('forgot_password.html')

    @app.route('/new_password', methods=['POST'])
    def new_password():
        return "hehe"

    return app
