from flask import Blueprint, flash, request, redirect, jsonify, render_template, url_for, session as session_flask
from .model import session, User


bp = Blueprint('auth', __name__, url_prefix='/auth')
user_in_database = session.query(User).all()


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/session', methods=['POST'])
def create_session():
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
    reset_email = request.form['reset_email']
    print(reset_email)
    return "yee"


@bp.route('/logout')
def logout():
    return redirect(url_for('auth.login'))


@bp.route('/register')
def register():
    return render_template('register.html')


@bp.route('/register/create', methods=['POST'])
def create_user():
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
