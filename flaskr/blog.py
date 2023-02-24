from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from flaskr.auth import login_required
from flaskr.database import get_cursor, close_cursor, commit

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_cursor()
    db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    posts = db.fetchall()

    close_cursor(db)

    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'É necessário um título.'

        if error is not None:
            flash(error)
        else:
            db = get_cursor()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (%s, %s, %s)',
                (title, body, g.user['id'])
            )
            commit()
            close_cursor(db)
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    db = get_cursor()
    db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = %s',
        (id,)
    )
    post = db.fetchone()
    close_cursor(db)

    if post is None:
        abort(404, f"Post id {id} não existe.")

    if g.user['adm'] == True:
        return post

    elif check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'É necessário um título.'

        if error is not None:
            flash(error)
        else:
            db = get_cursor()
            db.execute(
                'UPDATE post SET title = %s, body = %s'
                ' WHERE id = %s',
                (title, body, id)
            )
            commit()
            close_cursor(db)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_cursor()
    db.execute('DELETE FROM post WHERE id = %s', (id,))
    commit()
    close_cursor(db)
    return redirect(url_for('blog.index'))
