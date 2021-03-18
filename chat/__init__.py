from flask import Flask, render_template
from config import Config
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__)
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.config.from_object(Config)
    from . import auth
    from chat import flask_chat
    app.register_blueprint(flask_chat.bp)
    app.register_blueprint(auth.bp)
    socketio = SocketIO(app, async_mode='gevent')

    def messageReceived(methods=['GET', 'POST']):
        print('message was received!!!')

    @socketio.on('my event')
    def handle_my_custom_event(json, methods=['GET', 'POST']):
        print('received my event: ' + str(json))
        socketio.emit('my response', json, callback=messageReceived)

    @app.route('/')
    @app.route('/index')
    def index():
        return render_template('login.html')
    return app


def create_socket():
    app = create_app()
    socketio = SocketIO(app, async_mode='eventlet')
    return socketio
