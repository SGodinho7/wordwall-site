from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required

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

        if bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('core.index'))
        else:
            return 'Failed'


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

        user = User(username=username, email=email, password=password)

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('core.index'))
