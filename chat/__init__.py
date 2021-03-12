from flask import Flask, render_template, session


def init_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['DEBUG'] = True

    from . import auth
    app.register_blueprint(auth.bp)

    @app.route('/')
    def index():
        return render_template('base.html')

    @app.route('/forgot_password')
    def forgot_password():
        return render_template('forgot_password.html')
    return app
