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
        posts = Post.query.order_by(db.desc(Post.id_post))

        return render_template('core/index.html', posts=posts)
    elif request.method == 'POST' and current_user.is_authenticated:
        body = request.form.get('body')
        created_at = datetime.datetime.now().replace(microsecond=0)
        user = current_user

        post = Post(body=body, created_at=created_at, user=user)

        db.session.add(post)
        db.session.commit()

        return redirect(url_for('core.index'))

