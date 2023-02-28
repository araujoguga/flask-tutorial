import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.database import get_cursor, close_cursor, commit

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_cursor()
        error = None

        if not username:
            error = 'É necessário um usuário.'
        elif not password:
            error = 'É necessária uma senha.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password)),
                )
                commit()
                close_cursor(db)

            except db.IntegrityError:
                error = f"Usuário já existe."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_cursor()
        error = None
        db.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )
        user = db.fetchone()

        if user is None:
            error = 'Usuário ou senha incorretos.'
        elif not check_password_hash(user['password'], password):
            error = 'Usuário ou senha incorretos.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/change_password', methods=['GET', 'POST'])
def change_password():

    if request.method == 'POST':
        newpassword = request.form['newpassword']
        cnewpassword = request.form['cnewpassword']
        error = None

        if newpassword != cnewpassword:
            error = 'Senhas diferentes.'

        if error is None:
            try:
                db = get_cursor()
                db.execute(
                    'update user '
                    'set user.password = %s '
                    'where user.id = %s ',
                    (generate_password_hash(newpassword), g.user['id'])
                )
                commit()
                close_cursor(db)

                return redirect(url_for('auth.sucess'))

            except error:
                return redirect(url_for('auth.fail'))

        flash(error)

    return render_template('auth/change_password.html')


@bp.route('/change_password/sucess')
def sucess():

    return render_template('auth/sucess.html')


@bp.route('/change_password/fail')
def fail():

    return render_template('auth/fail.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db = get_cursor()
        db.execute(
            'SELECT * FROM user WHERE id = %s', (user_id,)
        )
        g.user = db.fetchone()
        close_cursor(db)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


def adm_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['adm'] == 0:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view


def master_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['master'] == 0:
            return redirect(url_for('index'))

        return view(**kwargs)

    return wrapped_view
