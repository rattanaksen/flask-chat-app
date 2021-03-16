from flask import Blueprint, render_template, url_for
from chat import create_app
from flask_socketio import SocketIO

bp = Blueprint('flask_chat', __name__)
app = create_app()
socketio = SocketIO(app)


@bp.route('/chat')
def chat():
    return render_template('chat.html')
