from chat import init_app
from flask_mail import Mail, Message
from .model import session, User
from flask import Blueprint, Flask, current_app, flash, request, redirect, jsonify, render_template, url_for, session as session_flask
import jwt


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/create_session', methods=['POST'])
def create_session():
    user_in_database = session.query(User).all()
    loginEmail = request.form['loginEmail']
    loginPassword = request.form['loginPassword']
    for email, password in user_in_database:
        if loginEmail == email:
            if loginPassword == password:
                return "Login success"
    flash("Incorrect email or password")
    return redirect(url_for('auth.login'))


@bp.route('/reset', methods=['POST'])
def reset():
    app = init_app()
    with app.app_context():
        reset_email = request.form['reset_email']
        user_in_database = session.query(User).all()
        for user_email in user_in_database:
            if reset_email in user_email.email:
                encoded_password = jwt.encode(
                    {"pas": user_email.password}, "secret", algorithm="HS256")
                mail = Mail(current_app)
                msg = Message("Reset Password", recipients=[reset_email])
                msg.body = f'http://127.0.0.1:5000/change_passoword?token={encoded_password}'
                mail.send(msg)
                flash("Email sent")
                return redirect('/auth/login')
    flash('Email does not exists')
    return redirect(url_for('auth.login'))


@bp.route('/create_new_password')
def create_new_password():
    return render_template('create_password.html')


@bp.route('/logout')
def logout():
    return redirect(url_for('auth.login'))


@bp.route('/register')
def register():
    return render_template('register.html')


@bp.route('/register/create', methods=['POST'])
def create_user():
    user_in_database = session.query(User).all()
    for each_user in user_in_database:
        if request.form['email'] in each_user.email:
            flash('Email is already exists')
            return redirect(url_for('auth.login'))
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    email = request.form['email']
    password = request.form['password']
    new_user = User(first_name=first_name, last_name=last_name,
                    email=email, password=password)
    session.add(new_user)
    session.commit()
    return redirect(url_for('auth.login'))
