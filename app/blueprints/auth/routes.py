from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app.app import db, bcrypt
from app.blueprints.auth.models import User

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/static')


@auth.route('/', methods=['GET'])
def index():
    return redirect(url_for('core.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('auth/login.html')
    elif request.method == 'POST':
        data = request.form
        email = data['email']
        password = data['password']

        user = User.query.filter(User.email == email).first()
        if user is None:
            return 'Failed - User does not exist.'

        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('core.index'))
        else:
            return 'Failed - Wrong password'


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('core.index'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'GET':
        return render_template('auth/signup.html')
    elif request.method == 'POST':
        data = request.form
        username = data['username']
        email = data['email']
        password = bcrypt.generate_password_hash(data['password'])

        if User.query.filter(User.email == email).first() is not None:
            return 'Failed - Email is already registered'

        user = User(username=username, email=email,
                    password=password, nickname=username, description='')

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('core.index'))


@auth.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    if request.method == 'GET':
        return render_template('auth/update.html')
    elif request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password')
        new_password = request.form.get('new-password')
        description = request.form.get('desc')

        if not bcrypt.check_password_hash(current_user.password, password):
            return 'Failed - Wrong current password'

        if User.query.filter(User.email == email).first() is not None and current_user.email != email:
            return 'Failed - E-mail is already registered'

        user = db.session.get(User, current_user.id_user)
        user.nickname = nickname
        user.email = email
        user.description = description
        if new_password != '':
            user.password = bcrypt.generate_password_hash(new_password)

        db.session.commit()

        return redirect(url_for('core.profile', username=current_user.username))
