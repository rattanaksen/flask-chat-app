from chat import init_app
from flask_mail import Mail, Message
from .model import session, User, JwtToken
from flask import Blueprint, make_response, Flask, current_app, flash, jsonify, request, Response, redirect, render_template, url_for
import jwt
from sqlalchemy import delete


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/register')
def register():
    return render_template('register.html')


@bp.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')


@bp.route('/login/create_session', methods=['POST'])
def create_session():
    login_email = request.form['loginEmail']
    login_password = request.form['loginPassword']
    user = session.query(User).filter_by(email=login_email).first()
    if user is None or not user.check_password(login_password):
        flash("Incorrect email or password")
        return redirect(url_for('auth.login'))
    return "login success"


@bp.route('/register/create', methods=['POST'])
def create_user():
    register_first_name = request.form['firstName']
    register_last_name = request.form['lastName']
    register_email = request.form['email']
    register_password = request.form['password']
    user = session.query(User).filter_by(email=register_email).first()
    if user is None:
        new_user = User(first_name=register_first_name,
                        last_name=register_last_name, email=register_email)
        new_user.set_password(register_password)
        session.add(new_user)
        session.commit()
        flash('Register Success!')
        return redirect(url_for('auth.login'))
    flash('Email is already exists!')
    return redirect(url_for('auth.login'))


@bp.route('/reset_password/check', methods=['POST'])
def check_reset_password():
    app = init_app()
    with app.app_context():
        reset_email = request.form['reset_email']
        user = session.query(User).filter_by(email=reset_email).first()
        if user is None:
            flash('Email does not exists!')
            return redirect(url_for('auth.login'))
        encoded_token = jwt.encode(
            {"email": user.get_email()}, "secret", algorithm="HS256")
        mail = Mail(current_app)
        msg = Message("Reset Password", recipients=[reset_email])
        msg.body = f'http://127.0.0.1:5000/auth/create_new_password?token={encoded_token}'
        mail.send(msg)
        session.add(JwtToken(jwt_token=encoded_token))
        session.commit()
        flash("Email sent")
        return redirect('/auth/login')


@bp.route('/create_new_password', methods=['GET', 'POST'])
def create_new_password():
    if request.method == 'POST':
        reset_token = request.cookies.get('jwt')
        new_password = request.form['new_password']
        try:
            decoded_token = jwt.decode(
                reset_token, "secret", algorithms=["HS256"])
            database_token = session.query(JwtToken).filter_by(
                jwt_token=reset_token).first()
            jwt_reset_token = database_token.jwt_token
            if jwt_reset_token is None:
                flash('Token is already Used!')
                redirect(url_for('auth.login'))
            reset_user_password = session.query(User).filter_by(
                email=decoded_token['email']).first()
            reset_user_password.set_password(new_password)
            session.delete(database_token)
            session.add(reset_user_password)
            session.commit()
            flash("Reset Success!")
            resp = make_response(redirect(url_for('auth.login')))
            resp.delete_cookie('jwt', path='/', domain='127.0.0.1')
            return resp
        except:
            flash('Invaild token!')
            return redirect(url_for('auth.login'))
    elif request.method == 'GET':
        reset_token = request.args.get('token')
        resp = make_response(render_template(
            'create_new_password.html'))
        resp.set_cookie('jwt', reset_token)
        return resp


@bp.route('/logout')
def logout():
    return redirect(url_for('auth.login'))
