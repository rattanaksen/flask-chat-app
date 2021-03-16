from flask import Blueprint, render_template, url_for

bp = Blueprint('flask_chat', __name__)


@bp.route('/chat')
def chat():
    return render_template('chat.html')
