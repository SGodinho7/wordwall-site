import datetime

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user

from app.app import db
from app.blueprints.core.models import Post

core = Blueprint('core', __name__, template_folder='templates',
                 static_folder='static', static_url_path='/static')


@core.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all()

        return render_template('core/index.html', posts=posts)
    elif request.method == 'POST' and current_user.is_authenticated:
        body = request.form.get('body')
        created_at = datetime.datetime.now()
        user_id = current_user.get_id()

        post = Post(body=body, created_at=created_at, user_id=user_id)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('core.index'))

