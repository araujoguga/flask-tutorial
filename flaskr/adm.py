import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from flaskr.auth import login_required, adm_required, master_required
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.database import get_cursor, close_cursor, commit


bp = Blueprint('adm', __name__, url_prefix='/adm')


@bp.route('/users')
@login_required
@adm_required
def users():
    db = get_cursor()
    db.execute(
        'SELECT id, username, adm '
        'from user '
        "WHERE username !='admin' "
        'ORDER BY id'
    )
    users = db.fetchall()
    close_cursor(db)

    return render_template('adm/index.html', users=users)


@bp.route('/master')
@login_required
@master_required
def master():
    db = get_cursor()
    db.execute(
        'SELECT id, username, adm '
        'from user '
        "WHERE username !='admin' "
        'ORDER BY id'
    )
    users = db.fetchall()
    close_cursor(db)

    return render_template('adm/master.html', users=users)


@bp.route('master/update/<int:id>/<int:profile>')
@login_required
@master_required
def update(id, profile):
    new_profile = False if profile else True
    db = get_cursor()
    db.execute(
        'update user '
        'set user.adm = %s '
        'where user.id = %s ',
        (new_profile, id)
    )
    commit()
    close_cursor(db)

    return redirect(url_for('.master'))


@bp.route('master/reset_password/<int:id>')
@login_required
@master_required
def reset_password(id):
    db = get_cursor()
    db.execute(
        'update user '
        'set user.password = %s '
        'where user.id = %s ',
        (generate_password_hash('padrao1'), id)
    )
    commit()
    close_cursor(db)

    return redirect(url_for('.master'))
